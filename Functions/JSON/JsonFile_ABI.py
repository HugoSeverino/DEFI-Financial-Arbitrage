from .JsonFile import JsonFile
import json
class JsonFile_ABI(JsonFile):

    
    def __init__(self,JsonFile):
        pass

    
    def ReturnJsonAsPythonReadable(self) -> None:
        with open(self) as Json: 
            ABI = json.load(Json)
            return ABI
