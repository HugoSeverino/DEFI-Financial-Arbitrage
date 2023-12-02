from .SQL_Init import SQL_Init
import mysql.connector
import os
from mysql.connector import Error


class SQL_Token(SQL_Init):

    def __init__(self):

        SQL_Password = os.getenv('SQL_Password')
              
        self._connexion = mysql.connector.connect(host="localhost",user="root",password=SQL_Password,database="mainet",port=3306)

        

    def Update_Database(self,token0,token1):
        
        self._cursor = self._connexion.cursor()

               
        try:
            self._cursor.execute("""INSERT IGNORE INTO TokenList (adrr) VALUES (%s), (%s)""",(token0,token1))
            self._connexion.commit()

        except Error as e:
            if e.errno == 1062:
                print("Token Already in DB")
            else:
                print(f"Error Creating Database: {e}")
                pass
    
    def Count(self):
    
        cursor = self._connexion.cursor()
        
        nb=cursor.execute('SELECT COUNT(*) FROM TokenList')
        nb=cursor.fetchall()[0][0]
        
        super().CloseConnexion()
        return nb
    
    def Update_Orphelin(self):

        cursor = self._connexion.cursor()

        query = """
        UPDATE TokenList
        SET orphelin = true
        WHERE adrr IN (
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
        SELECT COUNT(*) 
        FROM TokenList
        WHERE orphelin IS NOT true;
        """

        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        super().CloseConnexion()
        
        return result

        
        

        



