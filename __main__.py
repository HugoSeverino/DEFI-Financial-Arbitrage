from Functions import fetch_uniswap_pairs
from web3 import Web3
import os
from dotenv import load_dotenv

# Load secret .env file
load_dotenv()
# Store credentials
API_Keys = os.getenv('Infura_API')

infura = f'https://mainnet.infura.io/v3/{API_Keys}' #Infura API
#infura = 'http://localhost:8545' #ETH Local Node
web3 = Web3(Web3.HTTPProvider(infura))
fetch_uniswap_pairs(web3)


#tes