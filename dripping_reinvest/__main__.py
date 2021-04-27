import logging
import click
import json
from types import SimpleNamespace
from web3 import Web3
from web3.middleware import geth_poa_middleware

from . import die, exception_decorator, log
from .constants import INFURA_URL, POLL_INTERVAL, DB_JSON_FILE
from .database import Database
from .telegram import TelegramBot
from .dripping import DripStakingContract, DrippingAccount, DripTokenContract
from .reinvest import DrippingReinvest

"""
Click callback function
"""
def _load_config(ctx, param, value) -> SimpleNamespace:
    @exception_decorator(die_enabled=True)
    def wrapper(file: str):
        log.debug(f'Loading config: {file}')
        with open(file, 'r') as f:
            config = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
            required_configs = ['private_key']
            for c in required_configs:
                if not hasattr(config, c) or not getattr(config, c):
                    die(f'Missing required config: {c}')
            return config
    return wrapper(value)

"""
Initialize Web3 object and connect to infura url
"""
def _init_w3(infura_url: str) -> Web3:
    w3 = Web3(Web3.HTTPProvider(infura_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    if not w3.isConnected():
        die(f'Failed to connect to {infura_url}')
    return w3

@click.command()
@click.option('-c', '--config', 'config', nargs=1, type=click.Path(exists=True), callback=_load_config, required=True, help='Path to config .json file')
@click.option('-v', '--verbose', 'verbose', default=False, is_flag=True, help='Enable verbose output')
def main(config: SimpleNamespace, verbose: bool):
    log.setLevel(logging.DEBUG if verbose else logging.INFO)
    log.info('Dripping auto reinvest started. Press CTRL+C to exit')

    w3 = _init_w3(INFURA_URL)
    db = Database(DB_JSON_FILE)

    telegram_bot = None
    if  hasattr(config, 'telegram_token') and config.telegram_token \
    and hasattr(config, 'telegram_users') and config.telegram_users:
        telegram_bot = TelegramBot(db, w3, config.telegram_token, config.telegram_users)

    log.debug(f"Telegram bot {'enabled' if telegram_bot else 'disabled'}")

    dripping_account = DrippingAccount(DripStakingContract(w3), DripTokenContract(w3), config.private_key)
    log.debug(f'Using dripping account address: {dripping_account.address}')

    DrippingReinvest(db, w3, dripping_account).run_interval(POLL_INTERVAL)

if __name__ == '__main__':
    main()
