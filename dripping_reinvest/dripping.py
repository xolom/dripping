from typing import cast
from functools import wraps
from hexbytes import HexBytes
from eth_account.signers.local import LocalAccount
from web3 import Web3, contract

from . import Func, exception_decorator, log
from .constants import DRIP_STAKING_CONTRACT_ADDR, DRIP_STAKING_ABI_FILE
from .utils import calc_token_value
from .contract import Contract
from .token import DripTokenContract

"""
Dripping staking contract class for convinient usage of contract interaction
"""
class DripStakingContract(Contract):

    def __init__(self, w3: Web3) -> None:
        super().__init__(w3, DRIP_STAKING_CONTRACT_ADDR, DRIP_STAKING_ABI_FILE)

    @property
    def contract(self) -> contract.Contract:
        return self._contract

    @exception_decorator()
    def balance(self, address: str) -> int:
        return self._contract.functions.balanceOf(address).call()

    @exception_decorator()
    def dividends(self, address: str) -> int:
        return self._contract.functions.dividendsOf(address).call()

    @exception_decorator()
    def daily_estimate(self, address: str) -> int:
        return self._contract.functions.dailyEstimate(address).call()

    @exception_decorator()
    def reinvest(self, address: str, gwei: int, private_key: bytes) -> HexBytes:
        transaction = self._contract.functions.reinvest().buildTransaction({
            'from':     address,
            'gasPrice': self._w3.toWei(gwei, 'gwei'),
            'nonce':    self._w3.eth.get_transaction_count(address)
        })
        signed_tx = self._w3.eth.account.sign_transaction(transaction, private_key=private_key)
        tx = self._w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        log.debug(f'Processing transaction: {tx.hex()}')
        self._w3.eth.waitForTransactionReceipt(tx)
        return tx

"""
Dripping account class which uses DrippingContract in combination with a private key
to make interactions with wallet to the contract
"""
class DrippingAccount():

    def __init__(self,
                 staking_contract: DripStakingContract,
                 token_contract: DripTokenContract,
                 private_key: bytes) -> None:
        self._drip_staking_contract = staking_contract
        self._drip_token_contract   = token_contract
        self._account: LocalAccount = staking_contract.w3.eth.account.privateKeyToAccount(private_key)

    def _balance_decorator(func: Func) -> Func:
        @wraps(func)
        def wrapper(self):
            res = func(self) or 0
            return round(calc_token_value(res, self._drip_token_contract.decimals), 2)
        return cast(Func, wrapper)

    @property
    def address(self) -> str:
        return str(self._account.address)

    @property
    @_balance_decorator
    def balance(self) -> float:
        return self._drip_staking_contract.balance(self.address)

    @property
    @_balance_decorator
    def dividends(self) -> float:
        return self._drip_staking_contract.dividends(self.address)

    @property
    @_balance_decorator
    def daily_stimate(self) -> float:
        return self._drip_staking_contract.daily_estimate(self.address)

    def reinvest(self, gwei: int) -> HexBytes:
        return self._drip_staking_contract.reinvest(self.address, gwei, self._account.key)
