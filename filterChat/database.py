  
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
            self._cnn = mysql.connector.connect(
                                host = self._dbHost,
                                port = 3306,
                                db = self._dbName,
                                user = self._dbUser,
                                passwd = self._dbPass,
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
            return rows
        except (mysql.connector.errors.ProgrammingError) as e:
            print(e)

    def close(self):
        self._cur.close
        self._cnn.close
