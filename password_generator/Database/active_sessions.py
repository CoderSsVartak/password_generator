from datetime import datetime, date
from database import Database

class Active_Sessions:

    def __init__(self):

        self.d = Database()

    def create_session(self, username):

        flag = self.verify_user(username)
        
        #If user is not present in the active sessions already only then add the new user.
        if not flag:
            query = "INSERT INTO `user_info`.`active_sessions` (username) VALUES ('{}');".format(username)
            d = Database()
            db = d.connect()    
            result = d.execute(query)
            d.close(db)
            return(result)

        else:
            return False

    #Verify if user is present in the active sessions already or not. True if user is present
    def verify_user(self, username):

        #Verify that the username is of type string
        if not type(username) == str:
            return False

        #Verify if user is currently an active user or not
        query = "select username from `user_info`.`active_sessions`;"
        db = self.d.connect()
        data = self.d.fetch(query)
        self.d.close(db)
        try:
            if username in data:
                return True
            else:
                return False
        #If no user is present in the database
        except TypeError:
            return False       

    def add_otp(self, username, otp):

        flag = self.verify_user(username)

        #If the username is present add the OTP against his username only
        if flag:
            time, date = self.get_date_time()
            query = "update `user_info`.`active_sessions` set date='{}', time='{}', otp='{}' where username='{}';".format(date, time, otp, username)
            db = self.d.connect()
            result = self.d.execute(query)
            self.d.close(db)

            return(result)
        #If username is not present in the active sessions list
        else:
            return(False)

    #When the user enters the OTP, the OTP has to be verified to check if it was entered before it expired
    def verify_otp(self, username, otp):

        timenow, datenow = self.get_date_time()

        query = "select time, date, otp from `user_info`.`active_sessions` where username='{}';".format(username)
        db = self.d.connect()
        data = self.d.fetch(query)
        self.d.close(db)
        try:
            return (self.difference(datenow, timenow, data[1], data[0]) and otp == data[2])
        
        #If no OTP is sent
        except TypeError:
            return False


    #Date is the date when data was added in string format
    #time is the time when data was added in string format
    def difference(self, date_today, time_today, date_added, time_added):
        
        FMT = "%H:%M"
        sec = datetime.strptime(time_today, FMT)-datetime.strptime(time_added, FMT)

        return(date_today == date_added and sec.seconds <= 300)

    #date is the string format of (year,month,day) and time is the string format of the time of insertion
    #Whenever a login action is performed active session is to be created.
    

    def get_date_time(self):

        timenow = datetime.now().strftime("%H:%M")
        datenow = str(date.today())

        return (timenow, datenow)

    #When the user logs out, the session is stopped and the active session is ended
    def end_session(self, username):

        query = "delete from `user_info`.`active_sessions` where username='{}'".format(username)
        db = self.d.connect()
        result = self.d.execute(query)
        self.d.close(db)

        return result


#Driver Code
"""
a = Active_Sessions()
username = ""
OTP = ""

#(a.create_session(username)
#a.add_otp(username, OTP)
a.verify_otp(username, OTP)
print(a.end_session(username))
"""