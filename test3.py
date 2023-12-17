from web3 import Web3
from dotenv import load_dotenv
import os
import json
from eth_utils import to_checksum_address
from concurrent.futures import ThreadPoolExecutor

# Load secret .env file
load_dotenv()

# Store credentials
API = os.getenv('Quicknode_API')
quicknode = f"https://misty-white-sea.quiknode.pro/{API}"
web3 = Web3(Web3.HTTPProvider(quicknode))

# Chargement des adresses depuis le fichier JSON
with open('JSON/UniswapV2.json') as f:
    pool_addresses_set = set(to_checksum_address(entry["Pool"]) for entry in json.load(f))

# Get block information
block_number = 18783227
actual_block = web3.eth.block_number

def process_block(block_number):
    block_data = web3.eth.get_block(block_number, full_transactions=True)
    print(f"Number of transactions in block {block_number}: {len(block_data.transactions)}")

    # Convert input_data to a set for faster membership testing
    input_data_set = set(bytes.hex(tx['input']) for tx in block_data.transactions)

    # Check if any address in pool_addresses_set is contained in any element of input_data_set
    common_addresses = {address for address in pool_addresses_set if any(address in input_data for input_data in input_data_set)}

    print(f"Common addresses in block {block_number}: {common_addresses}")

    # Print transactions with "Pool" address in the input data
    for tx in block_data.transactions:
        input_data = bytes.hex(tx['input'])
        if any(address in input_data for address in common_addresses):
            print(f"Block Number: {block_number}")
            print(f"Transaction Hash: {tx.hash.hex()}")
            print(f"Pool Address Found: {input_data}")
            print("\n")

# Utilisez ThreadPoolExecutor pour paralléliser le traitement des blocs
with ThreadPoolExecutor() as executor:
    executor.map(process_block, range(block_number, actual_block + 1))
