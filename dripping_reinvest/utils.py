from typing import Optional
from web3 import Web3

from .token import WBNBTokenContract, BUSDTokenContract, BUSDLPTokenContract, DripTokenContract, DripLPTokenContract

"""
Checks if a string is a parsable float.
Returns a float on success, None otherwise
"""
def parse_float(string: str) -> Optional[float]:
    try:
        return float(string)
    except:
        return None

"""
Convert a contracts token amount to correct value with decimals
"""
def calc_token_value(tokens: int, decimals: int) -> float:
    return tokens * 10 ** -decimals

"""
Get BUSD per WBNB from LP contract
"""
def get_usd_per_bnb(w3: Web3) -> float:
    busd_lp        = BUSDLPTokenContract(w3)
    busd_lp_wbnb   = calc_token_value(busd_lp.reserves[0], WBNBTokenContract(w3).decimals)
    busd_lp_tokens = calc_token_value(busd_lp.reserves[1], BUSDTokenContract(w3).decimals)
    return busd_lp_tokens / busd_lp_wbnb

"""
Get DRIP per WBNB from Dripping LP contract
"""
def get_drip_per_bnb(w3: Web3) -> float:
    drip_lp        = DripLPTokenContract(w3)
    drip_lp_tokens = calc_token_value(drip_lp.reserves[0], DripTokenContract(w3).decimals)
    drip_lp_wbnb   = calc_token_value(drip_lp.reserves[1], WBNBTokenContract(w3).decimals)
    return drip_lp_tokens / drip_lp_wbnb

"""
Get BUSD per DRIP from BUSD and Dripping LP contracts
"""
def get_usd_per_drip(w3: Web3) -> float:
    return get_usd_per_bnb(w3) / get_drip_per_bnb(w3)
