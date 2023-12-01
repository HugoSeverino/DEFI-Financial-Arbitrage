from web3 import Web3

from ..JSON import JsonFile_ABI_V3,JsonFile_Data_ListePools
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from web3._utils.filters import construct_event_filter_params
from web3._utils.events import get_event_data

T = TypeVar('T')

class Fetch_EventsPairV3(Generic[T],ABC):

    
    def __init__(self,web3: Web3,Factory_adress,App):
        
        self._App = App
        self._w3 = web3
        print(f'Looking for {self._App} V3 Pairs')
        self._KindofEvent = "PoolCreated" #Get Kind of event vor V3 Pairs
        self._factory_abi = JsonFile_ABI_V3.ReturnJsonAsPythonReadable("JSON/PairV3.json") #Get Pools ABI
        self._fromblock = JsonFile_Data_ListePools.ReturnLastItemBlock(f'JSON/{App}V3.json') #Get Last Item Block, Return 0 if no Json
        self._factory = web3.eth.contract( Factory_adress,abi = self._factory_abi) #Creating Contract instance for factory
        self._event = self._factory.events[self._KindofEvent] #Creating event for parir creation
        self._toblock = web3.eth.block_number #Get ETH Last Block Number
  
    def fetch_events(self,event = None,argument_filters=None,from_block=None,to_block="latest",address=None,topics=None):
        
        if from_block is None:
            raise TypeError("Missing mandatory keyword argument to getLogs: from_Block")

        abi = self._event._get_event_abi()
        abi_codec = self._w3.codec

        # Set up any indexed event filters if needed
        argument_filters = dict()
        _filters = dict(**argument_filters)

        data_filter_set, event_filter_params = construct_event_filter_params(
            abi,
            abi_codec,
            contract_address=event.address,
            argument_filters=_filters,
            fromBlock=from_block,
            toBlock=to_block,
            address=address,
            topics=topics,
        )

        # Call node over JSON-RPC API
        logs = self._w3.eth.get_logs(event_filter_params)

        # Convert raw binary event data to easily manipulable Python objects
        for entry in logs:
            data = get_event_data(abi_codec, abi, entry)
            yield data

    def IterateOverBlocks(self):
        toblock = 0
        latest_block_number = self._toblock
        fromblock = self._fromblock

        while toblock < latest_block_number: #Slicing by 50k blocks to avoid Infura API limitation of 10k results

            if fromblock + 50000 > latest_block_number:
                toblock = latest_block_number
            else:
                toblock = fromblock + 50000
            events = list(self.fetch_events(self._event, from_block=fromblock+1,to_block=toblock))
            
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
            
            JsonFile_Data_ListePools.AddDatainJson(f'JSON/{self._App}V3.json',data_list)




            
