from web3 import Web3

from .events import fetch_events

import json

with open('JSON/ERC20.json') as mon_fichier:
    data = json.load(mon_fichier)


uniswap_factory =  Web3.toChecksumAddress("0x1f98431c8ad98523631ae4a59f267346ea31f984")
factory_abi_url = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":true,"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"FeeAmountEnabled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":true,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":false,"internalType":"int24","name":"tickSpacing","type":"int24"},{"indexed":false,"internalType":"address","name":"pool","type":"address"}],"name":"PoolCreated","type":"event"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"}],"name":"createPool","outputs":[{"internalType":"address","name":"pool","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"enableFeeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"","type":"uint24"}],"name":"feeAmountTickSpacing","outputs":[{"internalType":"int24","name":"","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint24","name":"","type":"uint24"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parameters","outputs":[{"internalType":"address","name":"factory","type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
erc20_abi_url = data

def fetch_uniswap_pairs(web3: Web3):
    """Fetch all trading pairs on Uniswap"""
    factory = web3.eth.contract( uniswap_factory,abi = factory_abi_url)
    events = list(fetch_events(factory.events.PoolCreated, from_block=0))

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
        

