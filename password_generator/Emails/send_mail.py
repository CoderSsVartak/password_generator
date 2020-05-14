from password_generator.Emails.custom_mail import Server_Mail
import password_generator.Security.OTP_generate as o

#Reason attribute is the server side attribute which describes the purpose of the mail
#Reason can have the following values: OTP, new_registration, reminder 

class Send_Mail:

    def __init__(self, receiver, reason, **kwargs):

        self.receiver = receiver
        self.reason = reason
        self.kwargs = kwargs
        self.sender = ""
        self.pswd = ""
        self.sent, self.extra = self.send()

    def send(self):

        #Variable that will be returned
        extra = ''
        if 'otp' in self.reason.lower():
            extra = o.otp()
            subject = "One Time Password sent by Password Generator"
            with open("password_generator/Emails/One Time Password.txt", "r") as file:
                content = file.read()
                content += extra
                
        
        #Integrate the user's username after once db is connected
        elif 'regist' in self.reason:
            subject = "Welcome user"
            with open("password_generator/Emails/new_registration.txt", "r") as file:
                content = file.read()
            username = ''
            for key, value in self.kwargs.items():
                if 'username' in key.lower():
                    username = value
            content += username
            extra = username

        #Integrate the account name once db is connected
        elif 'remind' in self.reason:
            subject = "Reminder to change password"
            with open("password_generator/Emails/reminder.txt", "r") as file:
                content = file.read()
            account_name = ''
            for key, value in self.kwargs.items():
                if 'account_name' in key.lower():
                    account_name = value
            content += account_name
            extra = account_name
        else:
            return False, extra

        content += "\nNot you? You can ignore this mail or register a complaint at "+self.sender
        s = Server_Mail(self.sender, self.receiver, subject, content, self.pswd)
        flag = s.send_mail()
        return(flag, extra)
        
        
"""
#Driver Code
#OTP
sent = Send_Mail("", "otp")

#Registration
sent = Send_Mail("", "register", username="")

#Reminder
sent = Send_Mail("", "register", account_name="")
"""
