import mysql.connector
class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query, params=None):
        if not self.connection:
            self.connect()
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        return result
    
    def execute_insert(self, query, params=None):
        if not self.connection:
            self.connect()
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor.lastrowid