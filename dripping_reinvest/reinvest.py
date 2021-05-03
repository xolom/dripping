from colorama import Fore, Style
from threading import Timer
from web3 import Web3

from . import log
from .constants import TRANSACTION_GWEI
from .dripping import DrippingAccount
from .utils import get_usd_per_drip
from .database import Database
from dripping_reinvest import database

"""
Reinvesting class which uses DrippingAccount
"""
class DrippingReinvest():

    def __init__(self, db: Database, w3: Web3, dripping_account: DrippingAccount) -> None:
        self._db                    = db
        self._w3                    = w3
        self._dripping_account      = dripping_account
        self._cached_balance        = None
        self._cached_dividends      = None
        self._cached_daily_estimate = None

    def run_interval(self, interval: int) -> None:
        self.run()
        Timer(interval, self.run_interval, [interval]).start()

    def run(self) -> None:
        balance       = self._dripping_account.balance
        dividends     = self._dripping_account.dividends
        daily_stimate = self._dripping_account.daily_stimate

        if not balance:
            log.error('Failed to fetch balance')
            return

        dividends_percent       = round(dividends / balance * 100, 2)
        daily_estimate_percent  = round(daily_stimate / balance * 100, 2)
        dividends_thres_reached = dividends_percent > self._db.dividends_threshold

        if balance != self._cached_balance or dividends != self._cached_dividends or daily_stimate != self._cached_daily_estimate:
            self._cached_balance        = round(balance, 2)
            self._cached_dividends      = round(dividends, 2)
            self._cached_daily_estimate = round(daily_stimate, 2)

            drip_price = get_usd_per_drip(self._w3)

            dividends_color = Fore.CYAN if dividends_thres_reached else ''
            dividends_reset = Style.RESET_ALL if dividends_color else ''
            log.sticky(f'Balance: {balance:.2f} DRIP / ${balance * drip_price:.2f}, '
                       f'{dividends_color}Dividends: {dividends:.2f} DRIP / ${dividends * drip_price:.2f} ({dividends_percent}%){dividends_reset}, '
                       f'Daily est: {daily_stimate:.2f} DRIP / ${daily_stimate * drip_price:.2f} ({daily_estimate_percent}%)')

        if dividends_thres_reached:
            log.info('Reinvesting')
            if self._dripping_account.reinvest(TRANSACTION_GWEI):
                log.info(f'{dividends:.2f} DRIP reinvested')
