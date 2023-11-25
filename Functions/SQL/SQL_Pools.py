from .SQL import SQL
import mysql.connector
import os
from dotenv import load_dotenv
SQL_Password = os.getenv('SQL_Password')

class SQL_Pools(SQL):

    def __init__(self):

        self._connexion = mysql.connector.connect(host="localhost",user="root",password="angusyoung",database="test",port=3306)

    def Add_Item(self,pools):

        cur = self._connexion.cursor()