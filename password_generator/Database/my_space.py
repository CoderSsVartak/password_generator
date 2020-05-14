from password_generator.Database.database import Database
from datetime import date


class My_Space:

    def __init__(self):
        self.d = Database()
    

    def create_space(self, username):
        
        flag = True

        
        if flag:
            query = "create table `my_space`.`{}`(account_name varchar(45) primary key not null, user_pass varchar(120) not null, date varchar(45));".format(username)
            db = self.d.connect()
            result = self.d.execute(query)
            self.d.close(db)

        return flag


    def add_password(self, username, account_name, user_pass):

        #insert password into the database
        query = "insert into `my_space`.`{}` values('{}', '{}', '{}');".format(username, account_name, user_pass.decode(), str(date.today()))
        db = self.d.connect()
        result = self.d.execute(query)
        self.d.close(db)

        return result

    def show_passwords(self, username):

        query = "select * from `my_space`.`{}`;".format(username)

        db = self.d.connect()
        result = self.d.fetch_multiple(query)
        self.d.close(db)

        return result

    def delete_passwords(self, username, account_name):

        query = "delete from `my_space`.`{}` where account_name='{}';".format(username, account_name)

        db = self.d.connect()
        result = self.d.execute(query)
        self.d.close(db)

        return result


#Driver Code
#m = My_Space()
#username, account_name, user_pass = '', '', ''
#print(m.create_space(username))
#print(m.add_password(username, account_name, user_pass))
#print(m.show_passwords(username))
#print(m.delete_passwords(username, account_name))