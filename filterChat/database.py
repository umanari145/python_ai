  
import os
import mysql.connector





class database:

    def __init__(self, dbInfo):
        self._dbHost = dbInfo['DB_HOST']
        self._dbName = dbInfo['DB_NAME']
        self._dbUser = dbInfo['DB_USER']
        self._dbPass = dbInfo['DB_PASS']
        if (self.connect()) :
            print("connect")


    def connect(self):
        try:
            self._cnn = mysql.connector.connect(host=os.environ['DB_HOST'],
                                port=3306,
                                db=os.environ['DB_NAME'],
                                user=os.environ['DB_USER'],
                                passwd=os.environ['DB_PASS'],
                                )
            self._cur = self._cnn.cursor(dictionary=True)
            self._cur.execute("SET NAMES latin1")
            return True
        except (mysql.connector.errors.ProgrammingError) as e:
            print (e)
            return False
    

    def select(self, sql, args=None):
        try:
            self._cur.execute(sql, args)
            rows = self._cur.fetchall()
            for row in rows:
                print(row)
        except (mysql.connector.errors.ProgrammingError) as e:
            print(e)

    def close(self):
        self._cur.close
        self._cnn.close
