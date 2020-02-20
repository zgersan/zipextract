import sqlite3
from datetime import datetime


class Context():
    def __init__(self, dbName):
        self.conn = sqlite3.connect('{}'.format(dbName))


    def CreateTable(self, table, param1, param2, param3):
        self.table = table
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS {} ({}, {}, {})""".format(self.table, param1, param2, param3))


    def SelectAll(self, table):
        self.table = table
        cursor = self.conn.cursor()

    def log(self, action, error, time):
        cursor = self.conn.cursor()
        self.conn.execute("""CREATE TABLE IF NOT EXISTS logImg (id INTEGER PRIMARY KEY, 
                                                                action TEXT, 
                                                                error TEXT, 
                                                                time TEXT)""")
        data = [(action, error, time)]
        self.conn.executemany("""INSERT INTO logImg(action, error, time) VALUES (?, ?, ?)""", data)
        self.conn.commit()

    def result_log(self, action, json_data):
        cursor = self.conn.cursor()
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS logResult (id INTEGER PRIMARY KEY, 
                                                                       action TEXT, 
                                                                       date_time TEXT, 
                                                                       json_data json)""")
        data = [(action, date_time, json_data)]
        self.conn.executemany("""INSERT INTO logResult(action, date_time, json_data) VALUES (?, ?, ?)""", data)
        self.conn.commit()

    def outfile_log(self, action, error, time):
        cursor = self.conn.cursor()
        self.conn.execute("""CREATE TABLE IF NOT EXISTS logoutfile (id INTEGER PRIMARY KEY, 
                                                                   action TEXT, 
                                                                   error TEXT, 
                                                                   time TEXT)""")
        data = [(action, error, time)]
        self.conn.executemany("""INSERT INTO logoutfile(action, error, time) VALUES (?, ?, ?)""", data)
        self.conn.commit()

    def count_file(self, fileNumber, count, time):
        cursor = self.conn.cursor()

        self.conn.execute("""CREATE TABLE IF NOT EXISTS logcount (id INTEGER PRIMARY KEY, 
                                                                        fileNumber TEXT, 
                                                                        count INTEGER, 
                                                                        time TEXT)""")

        data = [(fileNumber, count, time)]
        self.conn.executemany("""INSERT INTO logcount(fileNumber, count, time) VALUES (?, ?, ?)""", data)
        self.conn.commit()

    def check_file(self, fileNumber):
        cursor = self.conn.cursor()

        self.conn.execute("""CREATE TABLE IF NOT EXISTS logcount (id INTEGER PRIMARY KEY, 
                                                                                fileNumber TEXT, 
                                                                                count INTEGER, 
                                                                                time TEXT)""")

        cursor.execute("SELECT * FROM logcount WHERE fileNumber=?", (fileNumber,))
        rows = cursor.fetchall()

        if len(rows) > 0:
            return True
        return False