from pathlib import Path
_package_path = Path(__file__).parent

INFURA_URL                  = 'https://bsc-dataseed1.binance.org:443'
TRANSACTION_GWEI            = 5
POLL_INTERVAL               = 5 * 60.0 # seconds
DB_JSON_FILE                = _package_path / 'database.json'
DRIP_TOKEN_ABI_FILE         = _package_path / 'abi/drip_token_contract.json'
DRIP_STAKING_ABI_FILE       = _package_path / 'abi/drip_staking_contract.json'
DRIP_LP_TOKEN_ABI_FILE      = _package_path / 'abi/drip_lp_contract.json'
WBNB_TOKEN_ABI_FILE         = _package_path / 'abi/wbnb_contract.json'
BUSD_TOKEN_ABI_FILE         = _package_path / 'abi/busd_contract.json'
BUSD_LP_TOKEN_ABI_FILE      = _package_path / 'abi/busd_lp_contract.json'
DRIP_STAKING_CONTRACT_ADDR  = '0xD62466b881b8Cabf0B99b609E41f4d3B05F6ed10'
DRIP_TOKEN_CONTRACT_ADDR    = '0xa8A1a8d65D08Cb95b611E340C16464f7Bb9b75B8'
DRIP_LP_TOKEN_CONTRACT_ADDR = '0xdeD46b086eBB1245F32039E384ad0E4DBBb60cb0'
WBNB_TOKEN_CONTRACT_ADDR    = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
BUSD_TOKEN_CONTRACT_ADDR    = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
BUSD_LP_TOKEN_CONTRACT_ADDR = '0x1B96B92314C44b159149f7E0303511fB2Fc4774f'
