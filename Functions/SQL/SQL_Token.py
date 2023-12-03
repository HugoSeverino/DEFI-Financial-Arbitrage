from .SQL_Init import SQL_Init
import mysql.connector
import os
from mysql.connector import Error
from ..JSON import JsonFile_ABI


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

        print("Updating Tokens Orphelins Database...")

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
        UPDATE TokenList
        SET orphelin = false
        WHERE adrr IN (
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
        FROM TokenList
        WHERE orphelin IS NOT true;
        """

        cursor.execute(query)
        result = cursor.fetchall()[0][0]
        super().CloseConnexion()
        
        return result
    
    def Update_Error(self,web3):

        print("Updating Tokens Errors Database...")



        self._cursor = self._connexion.cursor()

        query = """
        SELECT adrr 
        FROM TokenList
        WHERE error IS NOT true AND error IS NOT false AND orphelin IS false;
        """
        

        self._cursor.execute(query)
        result = self._cursor.fetchall()
        
        print(f'{len(result)} Tokens to process')

        self._ERC20_abi = JsonFile_ABI.ReturnJsonAsPythonReadable("JSON/ERC20.json")

        for Token in result: 
            
            self._Adress = Token[0]
            try:
                self._Token_Contract_Instance = web3.eth.contract( self._Adress,abi = self._ERC20_abi)
                

                self._Symbols = self._Token_Contract_Instance.functions.symbol().call()

                self._Decimals = self._Token_Contract_Instance.functions.decimals().call()
                print(f'Inserting new Token Infos : Adress :{self._Adress} Symbols : {self._Symbols} with {self._Decimals} decimals')

                self._cursor.execute("""
                UPDATE TokenList 
                SET symb = %s, deci = %s, error = %s
                WHERE adrr =%s
                """,(self._Symbols,self._Decimals,False,self._Adress))

                self._connexion.commit()
            
            except Exception as e:

                self._cursor.execute("""
                UPDATE TokenList 
                SET error = %s 
                WHERE adrr =%s
                """,(True,self._Adress))
                self._connexion.commit()
                print(f"Error processing token {self._Adress}: {e}")

                continue


        super().CloseConnexion()

        
    



        
        

        



