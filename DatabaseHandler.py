import mysql.connector
from mysql.connector import errorcode

class DataBaseHandler:
    def __init__(self, host, user, password, database, table, plantData):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.plantData = plantData

        try:
            self.conn = mysql.connector.connect(
            host= self.host,
            user= self.user,
            password= self.password,
            database= self.database)
            self.cursor = self.conn.cursor()

        except mysql.connector.Error as e:
            print(f"Could not connect to database: {e}")