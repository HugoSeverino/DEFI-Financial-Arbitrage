from web3 import Web3


from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Fetch_Event(Generic[T],ABC):

    
    def __init__(self,web3: Web3,Factory_adress: Web3.toChecksumAddress):

        

        pass

    @abstractmethod
    def fetch_events(self):
        
        pass
           
