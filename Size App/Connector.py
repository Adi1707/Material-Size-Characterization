from getpass import getpass
from multiprocessing import connection
from colorama import Cursor
from mysql.connector import connect,Error


class Connector:
    def __init__(self):
        self.connection = connect(
            host = 'localhost',
            user = input("Enter UserName : "),
            password = getpass("Enter Password : "),
        )
        query = "create database learn1"
        q2 = "drop database learn2"
        cur = self.connection.cursor()
        cur.execute(query)
        print("Job Done!")

    def insert_data(self):
        pass
    
    #Fetch Data
    def fetch_data(self):
        query = "SELECT * FROM USER LEARN"
        cur = self.connection.cursor()
        cur.execute(query)
        for row in cur:
            for col in row:
                print(col)
        
        print("Job Done!")




rdbms = Connector()
