from .SQL import SQL
import mysql.connector
import os



class SQL_Pools(SQL):

    def __init__(self):

        SQL_Password = os.getenv('SQL_Password')
              
        self._connexion = mysql.connector.connect(host="localhost",user="root",password=SQL_Password,database="mainet",port=3306)

    def Create_Table(self,name):

        cursor = self._connexion.cursor()    
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name} (
    
        pool VARCHAR(255) PRIMARY KEY,
        token0 VARCHAR(255),
        token1 VARCHAR(255),
        fee integer,
        reserve0 float8,
        reserve1 float8,
        tickspacing integer,
        SQRTX96 integer,
        tick integer,
        liquidity integer,
        block integer
        );''')

        cursor.close()
        self._connexion.close()

    def Add_Item(self,pools):

        cur = self._connexion.cursor()

