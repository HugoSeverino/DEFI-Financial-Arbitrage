from .SQL_Init import SQL_Init
from .SQL_Token import SQL_Token
import mysql.connector
import os
from mysql.connector import Error


class SQL_Pools(SQL_Init):

    def __init__(self) -> None:

        SQL_Password = os.getenv('SQL_Password')
              
        self._connexion = mysql.connector.connect(host="localhost",user="root",password=SQL_Password,database="mainet",port=3306)

        

    def Update_Database(self,PoolsList,version) -> None:
        
        self._cursor = self._connexion.cursor()

        try:
            for pools in reversed(PoolsList):
                
                self._Pool = pools["Pool"]
                self._Token_0 = pools["Token_0"]
                self._Token_1 = pools["Token_1"]
                self._fee = pools["fee"]
                self._block = pools["block"]
                self._version = version

                if "tickSpacing" in pools:
                    self._tickSpacing = pools["tickSpacing"]
                    self._cursor.execute("""INSERT INTO PoolList (pool,token0,token1,fee,block_creation,version,tick) VALUES (%s,%s,%s,%s,%s,%s,%s)""",(self._Pool,self._Token_0,self._Token_1,self._fee,self._block,self._version,self._tickSpacing))
                else:
                    self._cursor.execute("""INSERT INTO PoolList (pool,token0,token1,fee,block_creation,version) VALUES (%s,%s,%s,%s,%s,%s)""",(self._Pool,self._Token_0,self._Token_1,self._fee,self._block,self._version))
                print(f'inserting Pool infos {pools}')
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

    def Count(self) -> int:

        cursor = self._connexion.cursor()
        nb=cursor.execute('SELECT COUNT(*) FROM PoolList')
        nb=cursor.fetchall()[0][0]
        
        super().CloseConnexion()
        return nb
    
    def Update_Orphelin(self) -> int:

        print("Updating Orphelins Pools Database...")
        cursor = self._connexion.cursor()

        query = """
        UPDATE PoolList
        SET orphelin = true
        WHERE token0 IN (
            SELECT token
            FROM (
                SELECT token0 AS token FROM PoolList
                UNION ALL
                SELECT token1 AS token FROM PoolList
            ) AS AllTokens
            GROUP BY token
            HAVING COUNT(token) = 1
        )
        OR token1 IN (
            SELECT token
            FROM (
                SELECT token0 AS token FROM PoolList
                UNION ALL
                SELECT token1 AS token FROM PoolList
            ) AS AllTokens
            GROUP BY token
            HAVING COUNT(token) = 1
        );
        """
        
        cursor.execute(query)
        self._connexion.commit()

        query = """
        UPDATE PoolList
        SET orphelin = false
        WHERE token0 IN (
            SELECT token
            FROM (
                SELECT token0 AS token FROM PoolList
                UNION ALL
                SELECT token1 AS token FROM PoolList
            ) AS AllTokens
            GROUP BY token
            HAVING COUNT(token) > 1
        )
        AND token1 IN (
            SELECT token
            FROM (
                SELECT token0 AS token FROM PoolList
                UNION ALL
                SELECT token1 AS token FROM PoolList
            ) AS AllTokens
            GROUP BY token
            HAVING COUNT(token) > 1
        );
        """

        cursor.execute(query)
        self._connexion.commit()
        
        
        query = """
        SELECT COUNT(*) 
        FROM PoolList
        WHERE orphelin IS NOT true;
        """

        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        super().CloseConnexion()
        
        return result
    
    def Update_Pools_Data(self,web3) -> None: #First time fetching all avaible pools refresh

        print("Updating Pools Data...")
        self._last_block = web3.eth.block_number #Even if some data will be updated with a block more recent we apply for all pools this value for block_last_refresh to save some api request

        print(f'Update data from block {self._last_block}')

        cursor = self._connexion.cursor()

        

    
    



