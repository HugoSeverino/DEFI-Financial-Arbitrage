from web3 import Web3
from dotenv import load_dotenv
import os
# Load secret .env file
load_dotenv()

# Store credentials
API_Keys = os.getenv('Infura_API')

infura = f'https://mainnet.infura.io/v3/{API_Keys}' #Infura API

web3 = Web3(Web3.HTTPProvider(infura))

data=(web3.eth.get_block(
18721636, full_transactions=True))

print(len(data.transactions))

for tx in data.transactions: 
    print(tx['from'])
    print(tx['to'])


data = web3.eth.get_transaction('0xa1273ec65267dd86ffb054517faa1c36da24d887f07533b3feed7e54499d3a48')
print(bytes.hex(data['input'])) 

print("1d42064Fc4Beb5F8aAF85F4617AE8b3b5B8Bd801" in bytes.hex(data['input']))
print(f"Is 1d42064Fc4Beb5F8aAF85F4617AE8b3b5B8Bd801 in input data: 1d42064Fc4Beb5F8aAF85F4617AE8b3b5B8Bd801 in bytes.hex({data['input']})")