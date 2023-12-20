from .JsonFile_ABI import JsonFile_ABI
import json
class JsonFile_ABI_V3(JsonFile_ABI):

    
    def __init__(self,JsonFile):
        super().__init__(JsonFile)


    
    def ReturnJsonAsPythonReadable(self) -> None:
        with open(self) as Json: 
            ABI = json.load(Json)
            return ABI
