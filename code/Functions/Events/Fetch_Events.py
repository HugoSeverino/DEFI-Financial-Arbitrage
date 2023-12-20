from web3 import Web3


from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Fetch_Event(Generic[T],ABC):

    @abstractmethod
    def __init__(self):

        pass

    @abstractmethod
    def fetch_events(self):
        
        pass

    @abstractmethod 
    def IterateOverBlocks(self):
        pass