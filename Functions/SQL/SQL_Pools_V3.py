from .SQL_Pools import SQL_Pools
import mysql.connector
import os



class SQL_Pools_V3(SQL_Pools):

    def __init__(self):

        super().__init__()
        self._cursor = self._connexion.cursor()

    def Update_Database(self,PoolsList):
        
        for pools in reversed(PoolsList):
            print(pools)
            self._Pool = pools["Pool"]
            self._Token_0 = pools["Token_0"]
            self._Token_1 = pools["Token_1"]
            self._fee = pools["fee"]
            self._block = pools["block"]
            self._version = 3
            self._cursor.execute("""INSERT INTO PoolList (pool,token0,token1,fee,block_creation) VALUES (%s,%s,%s,%s,%s)""",(self._Pool,self._Token_0,self._Token_1,self._fee,self._block))
        
        #super().CloseConnexion()



