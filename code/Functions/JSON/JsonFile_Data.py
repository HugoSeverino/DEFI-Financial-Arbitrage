from .JsonFile import JsonFile
import json
class JsonFile_Data(JsonFile):

    
    def __init__(self,JsonFile):
        super().__init__(JsonFile)

    
    def ReturnJsonAsPythonReadable(self) -> None:
        with open(self) as Json: 
            return json.load(Json)
