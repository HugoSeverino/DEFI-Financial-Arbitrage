from .SQL import SQL
import mysql.connector
import os
from mysql.connector import Error


class SQL_Init(SQL):

    def __init__(self):

        try:
            SQL_Password = os.getenv('SQL_Password')
                
            self._connexion = mysql.connector.connect(host="localhost",user="root",password=SQL_Password,port=3306)
            cursor = self._connexion.cursor()

            create_db_query = "CREATE DATABASE mainet"

            
            cursor.execute(create_db_query)

            print("Database Succefully created")

            cursor.close()
            self._connexion.close()
            
        except Error as e:
            print(f"Error Creating Database: {e}")
