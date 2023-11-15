from web3 import Web3

from .events import fetch_events

import json
from .JsonFile_ABI_V3 import JsonFile_ABI_V3




def fetch_pairs(web3: Web3,Factory_adress: Web3.toChecksumAddress) -> None:
    
    
    
    factory_abi = JsonFile_ABI_V3.ReturnJsonAsPythonReadable('JSON/Poolv3.json')
    print(factory_abi)
    try: #Fetch Last Block on data and choosing it as beginning 
        with open('JSON/data.json') as Pool_List: 
            Pool_List = json.load(Pool_List)
            fromblock = Pool_List[-1]["block"]
            print(f'Last block in database is {fromblock}')
    
    except:  #If files not exist, start from the beginning
        fromblock = 0
    
    latest_block_number = web3.eth.blockNumber #Get ETH Last Block Number

    print(f'Last Block in the Blockchain is {latest_block_number}')
    
    factory = web3.eth.contract( Factory_adress,abi = factory_abi)
    
    toblock = 0

    while toblock < latest_block_number: #Slicing by 250k blocks to avoid Infura API limitation of 10k results

        if fromblock + 250000 > latest_block_number:
            toblock = latest_block_number
        else:
            toblock = fromblock + 250000
        events = list(fetch_events(factory.events.PoolCreated, from_block=fromblock+1,to_block=toblock))
        print('Got', len(events), 'events',"fromblock",fromblock+1,"toblock",toblock)

        fromblock = toblock
        
        
        data_list = []  # List to store dictionaries for each event
        
        for ev in events[0:len(events)]:
            
            
            Pool_Infos= {
                "Pool" :  ev.args.pool,
                "Token_0" : ev.args.token0,
                "Token_1" : ev.args.token1,
                "fee" : ev.args.fee,
                "block" : ev.blockNumber,
            }
            
            
            data_list.append(Pool_Infos)
            #print(f'Adding pair {Pool_Infos}on Uniswap V3')
        #Opening Json, copy data, merge data, write json     
        try:
            with open('JSON/data.json', 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        combined_data = existing_data + data_list

        with open('JSON/data.json', 'w') as file:
            json.dump(combined_data, file, indent=2)
    
    

        

