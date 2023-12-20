from .JsonFile_ABI import JsonFile_ABI
import json
class JsonFile_ABI_V2(JsonFile_ABI):

    
    def __init__(self,JsonFile) -> None:
        super().__init__(JsonFile)

    
    def ReturnJsonAsPythonReadable(self) -> dict:
        with open(self) as Json: 
            ABI = json.load(Json)
            return ABI
