from .JsonFile import JsonFile
import json
class JsonFile_ABI(JsonFile):

    
    def __init__(self, json_file) -> None:
        super().__init__(json_file)

    
    def ReturnJsonAsPythonReadable(self) -> dict:
        with open(self) as Json: 
            ABI = json.load(Json)
            return ABI
