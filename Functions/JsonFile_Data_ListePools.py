from .JsonFile_Data import JsonFile_Data
import json



class JsonFile_Data_ListePools(JsonFile_Data):

    
    def __init__(self,JsonFile):
        pass

    
    def ReturnJsonAsPythonReadable(self) -> None:
        with open(self) as Json: 
            ABI = json.load(Json)
            return ABI
    
    def ReturnLastItemBlock(self) -> int:
        
        try: 
            with open(self) as JSON:
                Pool_List = json.load(JSON)
                return Pool_List[-1]["block"]
        except:
            return 0
