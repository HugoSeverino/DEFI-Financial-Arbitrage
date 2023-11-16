from Functions import fetch_pairs
from web3 import Web3
import os
from dotenv import load_dotenv

# Load secret .env file
load_dotenv()
# Store credentials
API_Keys = os.getenv('Infura_API')

infura = f'https://mainnet.infura.io/v3/{API_Keys}' #Infura API
#infura = 'http://localhost:8545' #ETH Local Node


web3 = Web3(Web3.HTTPProvider(infura)) # Creating Web3 instance 



UniswapV3_factory =  Web3.toChecksumAddress("0x1f98431c8ad98523631ae4a59f267346ea31f984")
SushiswapV3_factory =  Web3.toChecksumAddress("0xbACEB8eC6b9355Dfc0269C18bac9d6E2Bdc29C4F")
SushiswapV2_factory =  Web3.toChecksumAddress("0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac")

fetch_pairs(web3,UniswapV3_factory,"Uniswap","V3")
fetch_pairs(web3,SushiswapV3_factory,"Sushiswap","V3")
fetch_pairs(web3,SushiswapV2_factory,"Sushiswap","V2")



