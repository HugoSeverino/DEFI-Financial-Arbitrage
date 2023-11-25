from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class SQL(Generic[T],ABC):

    @abstractmethod
    def __init__(self):
        pass

    
    
