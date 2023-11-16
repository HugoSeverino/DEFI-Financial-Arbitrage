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



uniswap_factory =  Web3.toChecksumAddress("0x1f98431c8ad98523631ae4a59f267346ea31f984")


fetch_pairs(web3,uniswap_factory,"Uniswap","V3")



