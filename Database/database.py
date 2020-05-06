import mysql.connector as mysql

class Database:

    def __init__(self, localhost, username, dbpassword, port):

        self.hostname="localhost"
        self.username="root"
        self.dbpasswd="vartak@213"
        self.port="3306"
        
    #Connect to the database and tackle all the errors raised
    def connect(self):
        try:
            db = mysql.connect(host=self.hostname, user=self.username, passwd=self.dbpasswd, port=self.port, auth_plugin='mysql_native_password')
            return db
        except ConnectionRefusedError:
            return("Connection Refused")
        except mysql.errors.ProgrammingError:
            return("Programming error, access denied")

    #Close the established connection
    def close(self, db):
        db.close()
        return True
    
    #Execute the insertion queries which are asked by the user
    def execute(self, query):

        db = self.connect()
        try:
            cursor = db.cursor()
            cursor.execute(query)
            self.close(db)            
            del(cursor)
            db.commit()
            return True 

        except mysql.errors.IntegrityError:
            return False
    
    #Execute the fetch operatios from database asked by the user
    def fetch(self, query):

        db = self.connect()
        cursor = db.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        self.close(db)
        del(cursor)
        return(data)