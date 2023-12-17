from web3 import Web3
from dotenv import load_dotenv
import os

# Load secret .env file
load_dotenv()

# Store credentials
#API_Keys = os.getenv('Infura_API')
API = os.getenv('Quicknode_API')
#infura = f'https://mainnet.infura.io/v3/{API_Keys}'  # Infura API
quicknode = f"https://misty-white-sea.quiknode.pro/{API}"
web3 = Web3(Web3.HTTPProvider(quicknode))

# Get block information
block_number = 18721189

actual_block = web3.eth.block_number
address_to_check = "1d42064Fc4Beb5F8aAF85F4617AE8b3b5B8Bd801".lower()
for i in range (block_number,actual_block):
    block_data = web3.eth.get_block(i, full_transactions=True)
    print(f"Number of transactions in block {i}: {len(block_data.transactions)}")

    # Print sender and receiver addresses for each transaction in the block
    for tx in block_data.transactions:
        #print(f"Transaction Hash: {tx.hash.hex()}")
        #print(f"From: {tx['from']}")
        #print(f"To: {tx['to']}")
        #print(f"data : {bytes.hex(tx['input'])}")
        #print("\n")
        if address_to_check in bytes.hex(tx['input']):

        
            print(f"Transaction Hash: {tx.hash.hex()}")
            print("\n")

   
    
