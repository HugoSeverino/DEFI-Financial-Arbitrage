from .SQL import SQL
import mysql.connector
import os
from mysql.connector import Error


class SQL_Init(SQL):

    def __init__(self):

        SQL_Password = os.getenv('SQL_Password')
                
        self._connexion = mysql.connector.connect(host="localhost",user="root",password=SQL_Password,port=3306)

        self.CreateDatabase()
        self.CloseConnexion()

    def CreateDatabase(self):

        try:
            
            cursor = self._connexion.cursor()

            create_db_query = "CREATE DATABASE mainet"

            
            cursor.execute(create_db_query)

            print("Database Succefully created")

            
            
        except Error as e:

            if e.errno == 1007:
                print("Database 'mainet' already exists")
            else:
                print(f"Error Creating Database: {e}")

    def CloseConnexion(self):

        if self._connexion.is_connected():

            self._connexion.close()
            print("Connection closed.")

