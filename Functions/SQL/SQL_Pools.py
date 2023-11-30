from .SQL import SQL
import mysql.connector
import os



class SQL_Pools(SQL):

    def __init__(self):

        SQL_Password = os.getenv('SQL_Password')
              
        self._connexion = mysql.connector.connect(host="localhost",user="root",password="angusyoung",database="mainet",port=3306)

    

        

        
    
    def CloseConnexion(self):

        if self._connexion.is_connected():

            self._connexion.close()
            print("Connection closed.")

    

