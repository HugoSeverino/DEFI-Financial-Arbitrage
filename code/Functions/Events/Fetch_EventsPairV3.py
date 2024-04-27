from web3 import Web3

from ..JSON import JsonFile_ABI_V3,JsonFile_Data_ListePools
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Dict, Any
from web3._utils.filters import construct_event_filter_params
from web3._utils.events import get_event_data

T = TypeVar('T')

class Fetch_EventsPairV3(Generic[T],ABC):

    
    def __init__(self,web3: Web3,Factory_adress: str,App: str) -> None:
        
        self._App: str = App
        self._w3: Web3 = web3
        print(f'Looking for {self._App} V3 Pairs')
        self._KindofEvent: str = "PoolCreated" #Get Kind of event vor V3 Pairs
        self._factory_abi: Dict[str, Any]  = JsonFile_ABI_V3.ReturnJsonAsPythonReadable("JSON/PairV3.json") #Get Pools ABI
        self._fromblock: int = JsonFile_Data_ListePools.ReturnLastItemBlock(f'JSON/{App}V3.json') #Get Last Item Block, Return 0 if no Json
        self._factory: Web3.eth.contract = web3.eth.contract( Factory_adress,abi = self._factory_abi) #Creating Contract instance for factory
        self._event: Any = self._factory.events[self._KindofEvent] #Creating event for parir creation
        self._toblock: int = web3.eth.block_number #Get ETH Last Block Number
  
    def fetch_events(self, event: Any = None, argument_filters: Dict[str, Any] = None, from_block: int = None, to_block: str = "latest", address: str = None, topics: List[str] = None) -> List[Dict[str, Any]]:
        
        if from_block is None:
            raise TypeError("Missing mandatory keyword argument to getLogs: from_Block")

        abi: Dict[str, Any] = self._event._get_event_abi()
        abi_codec: Any  = self._w3.codec

        # Set up any indexed event filters if needed
        argument_filters: Dict[str, Any] = dict()
        _filters: Dict[str, Any] = dict(**argument_filters)

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
        logs: List[Dict[str, Any]] = self._w3.eth.get_logs(event_filter_params)

        # Convert raw binary event data to easily manipulable Python objects
        for entry in logs:
            data: Dict[str, Any] = get_event_data(abi_codec, abi, entry)
            yield data

    def IterateOverBlocks(self) -> None:
        toblock: int = 0
        latest_block_number: int = self._toblock
        
        fromblock: int = self._fromblock
        print(latest_block_number,fromblock)
        while toblock < latest_block_number: #Slicing by 5k blocks to avoid Infura API limitation results

            if fromblock + 60000 > latest_block_number:
                toblock = latest_block_number
            else:
                toblock = fromblock + 60000
            print(fromblock+1,toblock)    
            events: List[Dict[str, Any]] = list(self.fetch_events(self._event, from_block=fromblock+1,to_block=toblock))
            
            print('Got', len(events), 'events',"fromblock",fromblock+1,"toblock",toblock)

            fromblock = toblock
            
            
            data_list: List[Dict[str, Any]] = []  # List to store dictionaries for each event
            
            for ev in events[0:len(events)]:
                
                
                Pool_Infos: Dict[str, Any] = {
                    "Pool" :  ev.args.pool,
                    "Token_0" : ev.args.token0,
                    "Token_1" : ev.args.token1,
                    "fee" : ev.args.fee,
                    "block" : ev.blockNumber,
                    "tickSpacing" : ev.args.tickSpacing,
                }

                data_list.append(Pool_Infos)
            
            JsonFile_Data_ListePools.AddDatainJson(f'JSON/{self._App}V3.json',data_list)




            
