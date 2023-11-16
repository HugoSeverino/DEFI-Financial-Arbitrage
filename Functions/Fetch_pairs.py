from web3 import Web3

from .events import fetch_events

import json
from .JsonFile_ABI_V3 import JsonFile_ABI_V3
from .JsonFile_ABI_V2 import JsonFile_ABI_V2
from .JsonFile_Data_ListePools import JsonFile_Data_ListePools



def fetch_pairs(web3: Web3,Factory_adress: Web3.toChecksumAddress,App,Version) -> None:
    
    print(f'Looking for Pairs in {App}{Version}')
    if Version == "V3":
        factory_abi = JsonFile_ABI_V3.ReturnJsonAsPythonReadable(f'JSON/Pair{Version}.json') #Get Pools ABI
        KindofEvent = "PoolCreated"
    if Version == "V2": 
        factory_abi = JsonFile_ABI_V2.ReturnJsonAsPythonReadable(f'JSON/Pair{Version}.json') #Get Pools ABI
        KindofEvent = "PairCreated"
    
    
    fromblock = JsonFile_Data_ListePools.ReturnLastItemBlock(f'JSON/{App}{Version}.json') #Get Last Item Block, Return 0 if no Json
    
    latest_block_number = web3.eth.blockNumber #Get ETH Last Block Number

    print(f'Last Block in the Blockchain is {latest_block_number}')
    
    factory = web3.eth.contract( Factory_adress,abi = factory_abi)
    
    toblock = 0

    while toblock < latest_block_number: #Slicing by 50k blocks to avoid Infura API limitation of 10k results

        if fromblock + 50000 > latest_block_number:
            toblock = latest_block_number
        else:
            toblock = fromblock + 50000
        events = list(fetch_events(factory.events[KindofEvent], from_block=fromblock+1,to_block=toblock))
        print('Got', len(events), 'events',"fromblock",fromblock+1,"toblock",toblock)

        fromblock = toblock
        
        
        data_list = []  # List to store dictionaries for each event
        
        for ev in events[0:len(events)]:
            
            if Version =="V3":
                Pool_Infos= {
                    "Pool" :  ev.args.pool,
                    "Token_0" : ev.args.token0,
                    "Token_1" : ev.args.token1,
                    "fee" : ev.args.fee,
                    "block" : ev.blockNumber,
                }
            
            if Version =="V2":
                Pool_Infos= {
                    "Pool" :  ev.args.pair,
                    "Token_0" : ev.args.token0,
                    "Token_1" : ev.args.token1,
                    "fee" : 3000,
                    "block" : ev.blockNumber,
                }
            
            
            data_list.append(Pool_Infos)
            #print(f'Adding pair {Pool_Infos}on Uniswap V3')
        #Opening Json, copy data, merge data, write json     
        try:
            with open(f'JSON/{App}{Version}.json', 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        combined_data = existing_data + data_list

        with open(f'JSON/{App}{Version}.json', 'w') as file:
            json.dump(combined_data, file, indent=2)
    
    

        

