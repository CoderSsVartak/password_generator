from .database import Database
import re

#Database: user_info: Stores tables related to user information
                #Table: user_login: stores login information
                    # (user_id int unique auto increement, username varchar primary key unique, Full_name varchar not null, user_pass varchar not null, email varchar not null, security_qns varchar not null, security_qns_ans varchar not null)


#Login information given by the user which has to be first validated for any noise and then checked if present in db
#If username is present, check the password and if it matches then return True
#To register first the information entered by the user is evaluated to find for any unwanted characters.
#if all clear then value is inserted into the db

#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
class Login:

    def __init__(self, user, password, d):

        self.user = user
        self.password = password
        self.login = self.get_user_details(d)

    def get_user_details(self, d):

        #Check both username and password if any unwanted characters are present
        validate = all([self.text_validate(self.user), self.text_validate(self.password)])
        
        if validate:
            query = "select username, user_pass from user_info.user_login where username='"+self.user+"' limit 1;"
            data = d.fetch(query)
            data = self.user_validation(data)
            return data
        else:
            return("Unwanted Characters present")

    def text_validate(self, answer):

        if "\\" in answer:
            return False

        sym, word = bool(re.search(r"['\"]", answer)), bool(re.search(r'[a-zA-Z0-9]', answer))
        temp = [not sym, word]
        return all(temp)

    def user_validation(self, data):

        if data[1] == self.password:
            return True
        else:
            return False


#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
class Register:
    def __init__(self, d, username, Full_name, user_pass, email, security_qns, security_qns_ans):

        self.username = username
        self.Full_name = Full_name
        self.user_pass = user_pass
        self.email = email
        self.security_qns = security_qns
        self.security_qns_ans = security_qns_ans
        self.flag = all([self.text_validate(self.username), self.text_validate(self.Full_name), self.text_validate(self.user_pass),self.text_validate(self.security_qns_ans)])
        self.insert_done = self.insert(d)
    
    def text_validate(self, answer):

        if "\\" in answer:
            return False

        sym, word = bool(re.search(r"['\"]", answer)), bool(re.search(r'[a-zA-Z0-9]', answer))
        temp = [not sym, word]
        return all(temp)

    def insert(self, d):

        if self.flag:

            query = "INSERT INTO `user_info`.`user_login` (`username`, `Full_name`, `user_pass`, `security_qns`, `security_qns_ans`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(self.username, self.Full_name, self.user_pass, self.email, self.security_qns, self.security_qns_ans)
            result = d.execute(query)
            return result

        else:
            return(False)



#Backslash is accepted when it follows certain characters. Check that
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#DB variables
localhost, username, dbpassword, port = "localhost", "root", "vartak@213", 3306
d = Database(localhost, username, dbpassword, port)

#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#Driver Code for Register
"""
username, Full_name, password, security_qns, security_qns_ans = "Srushti", "srushti", "im_srm@2403", "Hello?", "c"
r = Register(d, username, Full_name, password, security_qns, security_qns_ans)
print(r.insert_done)
"""
#-----------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
#Driver Code for Login
"""
user = "Srushti"
password = "im_srm@2403"
l = Login(user, password, d)
print(l.login)
"""