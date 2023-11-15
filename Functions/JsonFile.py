from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class JsonFile(Generic[T],ABC):

    @abstractmethod
    def __init__(self,JsonFile :T):
        pass

    @abstractmethod
    def ReturnJsonAsPythonReadable(self,JsonFile :T) -> None:
        pass

    
