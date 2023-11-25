from .JsonFile_Data import JsonFile_Data
import json



class JsonFile_Data_ListePools(JsonFile_Data):

    
    def __init__(self,JsonFile) -> None:
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
    
    def AddDatainJson(self,data):
        try:
            with open(self, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        combined_data = existing_data + data

        with open(self, 'w') as file:
            json.dump(combined_data, file, indent=2)
