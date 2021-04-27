import json
from pathlib import Path
from web3 import Web3

from . import exception_decorator

"""
Contract base class
"""
class Contract():

    def __init__(self, w3: Web3, contract_addr: str, abi_json: Path) -> None:
        self._w3 = w3
        self._contract = self._w3.eth.contract(w3.toChecksumAddress(contract_addr), abi=self.load_abi(abi_json))

    @exception_decorator(die_enabled=True)
    def load_abi(self, json_file: str) -> dict:
        with open(json_file) as f:
            return json.load(f)

    @property
    def w3(self) -> Web3:
        return self._w3

"""
Token contract base class
"""
class TokenContract(Contract):

    def __init__(self, w3: Web3, contract_addr: str, abi_json: Path) -> None:
        super().__init__(w3, contract_addr, abi_json)

    @property
    @exception_decorator()
    def decimals(self) -> int:
        return self._contract.functions.decimals().call()

"""
LP token contract base class
"""
class LPTokenContract(TokenContract):

    def __init__(self, w3: Web3, contract_addr: str, abi_json: Path) -> None:
        super().__init__(w3, contract_addr, abi_json)

    @property
    @exception_decorator()
    def reserves(self):
        return self._contract.functions.getReserves().call()
