from .SQL_Pools import SQL_Pools
import mysql.connector
import os
from mysql.connector import Error


class SQL_Pools_V3(SQL_Pools):

    def __init__(self):

        super().__init__()
        

    def Update_Database(self,PoolsList):
        
        self._cursor = self._connexion.cursor()

        try:
            for pools in reversed(PoolsList):
                print(pools)
                self._Pool = pools["Pool"]
                self._Token_0 = pools["Token_0"]
                self._Token_1 = pools["Token_1"]
                self._fee = pools["fee"]
                self._block = pools["block"]
                self._version = 3
                self._cursor.execute("""INSERT INTO PoolList (pool,token0,token1,fee,block_creation) VALUES (%s,%s,%s,%s,%s)""",(self._Pool,self._Token_0,self._Token_1,self._fee,self._block))
                self._connexion.commit()

        except Error as e:

            if e.errno == 1062:
                print("All items enter in DB, continue")
            else:

                print(f"Error Creating Database: {e}")

        super().CloseConnexion()



