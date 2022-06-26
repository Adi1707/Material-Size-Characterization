from Image_Pr import Image_Pr as ip
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from getpass import getpass
from multiprocessing import connection
from mysql.connector import connect

class Database(ip):
    def __init__(self):
        self.connection = connect(
            host = 'localhost',
            user = input("Enter User ID: "),
            password = getpass("Enter Password: "),
        )

        query = "CREATE DATABASE GRAIN_DATA"
        query2 = "USE GRAIN_DATA"
        query3 = "CREATE TABLE GRAIN_DETAILS"
        cur = self.connection.cursor()
        cur.execute(query)
        cur.execute(query2)
        cur.execute(query3)
        print("DataBase Created")



    def image_data(self):
        obj1 = ip()
        pd_df = obj1.obtain_data()
        sqlEngine = create_engine('mysql+pymysql://root:1707@localhost:3306/GRAIN_DATA')
        dbConnection = sqlEngine.connect()

        try:
            frame = pd_df.to_sql(GRAIN_DETAILS , dbConnection , if_exists='fail')
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(e)
        else:
            print("Job Done!")
        finally:
            dbConnection.close()

        



obj = Database()
