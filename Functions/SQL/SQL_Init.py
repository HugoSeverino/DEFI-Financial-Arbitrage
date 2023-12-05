from .SQL import SQL
import mysql.connector
import os
from mysql.connector import Error


class SQL_Init(SQL):

    def __init__(self):

        SQL_Password = os.getenv('SQL_Password')
                
        self._connexion = mysql.connector.connect(host="localhost",user="root",password=SQL_Password,port=3306)

        self.CreateDatabase()
        self._connexion = mysql.connector.connect(host="localhost",user="root",password=SQL_Password,database="mainet",port=3306)
        self.CreateTable()
        self.CloseConnexion()

    def CreateDatabase(self):

        try:
            
            cursor = self._connexion.cursor()

            create_db_query = "CREATE DATABASE mainet"

            
            cursor.execute(create_db_query)

            print("Database Succefully created")

            
            
        except Error as e:

            if e.errno == 1007:
                print("Database 'mainet' already exists, continue")
            else:
                print(f"Error Creating Database: {e}")
    
    def CreateTable(self):
    
        cursor = self._connexion.cursor()    
        cursor.execute('''CREATE TABLE IF NOT EXISTS PoolList (
    
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
        block_creation integer,
        block_last_use integer,
        version integer,
        orphelin boolean,
        block_last_refresh integer,
        t0_t1 float8,
        t1_t0 float8
        );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS TokenList (
    
        adrr VARCHAR(255) PRIMARY KEY,
	    symb VARCHAR(255),
	    deci integer,
        error boolean,
        orphelin boolean
        );''')

        #cursor.execute('''ALTER TABLE PoolList ADD CONSTRAINT FK_Token0 FOREIGN KEY (token0) REFERENCES TokenList(adrr); ALTER TABLE PoolList ADD CONSTRAINT FK_Token1 FOREIGN KEY (token1) REFERENCES TokenList(adrr);''', multi=True)

    def CloseConnexion(self):

        if self._connexion.is_connected():

            self._connexion.close()
            print("Connection closed.")

