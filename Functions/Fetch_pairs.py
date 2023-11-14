from web3 import Web3

from .events import fetch_events

import json

with open('JSON/ERC20.json') as ERC20: #Importing ERC20 ABI structure
    erc20_abi_url = json.load(ERC20)

with open('JSON/Poolv3.json') as Poolv3: #Importing Poolv3 ABI structure
    factory_abi_url = json.load(Poolv3)





def fetch_pairs(web3: Web3,Factory_adress: Web3.toChecksumAddress,fromblock,toblock):
    """Fetch all trading pairs on Uniswap"""
    factory = web3.eth.contract( Factory_adress,abi = factory_abi_url)
    events = list(fetch_events(factory.events.PoolCreated, from_block=0,to_block=toblock))

    print('Got', len(events), 'events')
    
    # Each event.args is presented as AttrbuteDict
    # AttributeDict({'args': AttributeDict({'token0': '0x607F4C5BB672230e8672085532f7e901544a7375', 'token1': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'pair': '0x6d57a53A45343187905aaD6AD8eD532D105697c1', '': 94}), 'event': 'PairCreated', 'logIndex': 7, 'transactionIndex': 2, 'transactionHash': HexBytes('0xa0ce4b0db9bbf7887f09c4b35ec1167144b06f69fbbea6d6a163a72db28175d8'), 'address': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f', 'blockHash': HexBytes('0xf269a89cf729781bfa8e8ec421f8eefbf13e1fecd22b4118c1304d360832ef20'), 'blockNumber': 10092190})
    for ev in events[0:len(events)]:
        
        tok0=ev.args.token0
        tok1=ev.args.token1
        pool=ev.args.pool
        fee=ev.args.fee
        block=ev.blockNumber

        

        
        
        print(f'Adding pair {tok0}-{tok1} on Uniswap V3')
        

