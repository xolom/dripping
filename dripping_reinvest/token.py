from web3 import Web3

from .contract import TokenContract, LPTokenContract
from .constants import (
    DRIP_TOKEN_CONTRACT_ADDR, DRIP_TOKEN_ABI_FILE,
    DRIP_LP_TOKEN_CONTRACT_ADDR, DRIP_LP_TOKEN_ABI_FILE,
    WBNB_TOKEN_CONTRACT_ADDR, WBNB_TOKEN_ABI_FILE,
    BUSD_TOKEN_CONTRACT_ADDR, BUSD_TOKEN_ABI_FILE,
    BUSD_LP_TOKEN_CONTRACT_ADDR, BUSD_LP_TOKEN_ABI_FILE
)

"""
Dripping token contract class for convinient usage of contract interaction
"""
class DripTokenContract(TokenContract):
    def __init__(self, w3: Web3) -> None:
        super().__init__(w3, DRIP_TOKEN_CONTRACT_ADDR, DRIP_TOKEN_ABI_FILE)

"""
Cake-LP token contract class for convinient usage of contract interaction
"""
class DripLPTokenContract(LPTokenContract):
    def __init__(self, w3: Web3) -> None:
        super().__init__(w3, DRIP_LP_TOKEN_CONTRACT_ADDR, DRIP_LP_TOKEN_ABI_FILE)

"""
WBNB token contract class for convinient usage of contract interaction
"""
class WBNBTokenContract(TokenContract):
    def __init__(self, w3: Web3) -> None:
        super().__init__(w3, WBNB_TOKEN_CONTRACT_ADDR, WBNB_TOKEN_ABI_FILE)

"""
BUSD token contract class for convinient usage of contract interaction
"""
class BUSDTokenContract(TokenContract):
    def __init__(self, w3: Web3) -> None:
        super().__init__(w3, BUSD_TOKEN_CONTRACT_ADDR, BUSD_TOKEN_ABI_FILE)

"""
BUSD LP token contract class for convinient usage of contract interaction
"""
class BUSDLPTokenContract(LPTokenContract):
    def __init__(self, w3: Web3) -> None:
        super().__init__(w3, BUSD_LP_TOKEN_CONTRACT_ADDR, BUSD_LP_TOKEN_ABI_FILE)

