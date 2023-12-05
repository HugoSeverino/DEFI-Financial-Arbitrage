from web3 import Web3
from dotenv import load_dotenv
import os
# Load secret .env file
load_dotenv()

# Store credentials
API_Keys = os.getenv('Infura_API')

infura = f'https://mainnet.infura.io/v3/{API_Keys}' #Infura API

web3 = Web3(Web3.HTTPProvider(infura))

data=(web3.eth.get_block(3420930, full_transactions=True))

print(len(data.transactions))

for tx in data.transactions: 
    print(tx['from'])
    print(tx['to'])
    