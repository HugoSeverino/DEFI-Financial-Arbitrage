from web3 import Web3
from dotenv import load_dotenv
import os

# Load secret .env file
load_dotenv()

# Store credentials
API_Keys = os.getenv('Infura_API')

infura = f'https://mainnet.infura.io/v3/{API_Keys}'  # Infura API

web3 = Web3(Web3.HTTPProvider(infura))

# Get block information
block_number = 18721636
block_data = web3.eth.get_block(block_number, full_transactions=True)

print(f"Number of transactions in block {block_number}: {len(block_data.transactions)}")

# Print sender and receiver addresses for each transaction in the block
for tx in block_data.transactions:
    print(f"Transaction Hash: {tx.hash.hex()}")
    print(f"From: {tx['from']}")
    print(f"To: {tx['to']}")
    print("\n")

# Get transaction information by hash
tx_hash = '0xa1273ec65267dd86ffb054517faa1c36da24d887f07533b3feed7e54499d3a48'
tx_data = web3.eth.get_transaction(tx_hash)

# Print input data and check if a specific address is in the input data
print(f"Transaction Input Data: {bytes.hex(tx_data['input'])}")
address_to_check = "1d42064Fc4Beb5F8aAF85F4617AE8b3b5B8Bd801".lower()
print(f"Is {address_to_check} in input data: {address_to_check in bytes.hex(tx_data['input'])}")
