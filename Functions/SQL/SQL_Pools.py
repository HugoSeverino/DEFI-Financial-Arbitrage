from .SQL_Init import SQL_Init
from .SQL_Token import SQL_Token
import mysql.connector
import os
from mysql.connector import Error


class SQL_Pools(SQL_Init):

    def __init__(self):

        SQL_Password = os.getenv('SQL_Password')
              
        self._connexion = mysql.connector.connect(host="localhost",user="root",password="angusyoung",database="mainet",port=3306)

        

    def Update_Database(self,PoolsList,version):
        
        self._cursor = self._connexion.cursor()

        try:
            for pools in reversed(PoolsList):
                
                self._Pool = pools["Pool"]
                self._Token_0 = pools["Token_0"]
                self._Token_1 = pools["Token_1"]
                self._fee = pools["fee"]
                self._block = pools["block"]
                self._version = version
                print(f'inserting Pool infos {pools}')
                self._cursor.execute("""INSERT INTO PoolList (pool,token0,token1,fee,block_creation,version) VALUES (%s,%s,%s,%s,%s,%s)""",(self._Pool,self._Token_0,self._Token_1,self._fee,self._block,self._version))
                self._connexion.commit()
                print(f'inserting tokens in TokenList')
                SQL_Token.Update_Database(self,self._Token_0,self._Token_1)

        except Error as e:

            if e.errno == 1062:
                print("All items enter in DB, continue")
            else:
                print(f"Error Creating Database: {e}")
                pass

        super().CloseConnexion()



