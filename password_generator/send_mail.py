from Emails.custom_mail import Server_Mail
import Security.OTP_generate as o

#Reason attribute is the server side attribute which describes the purpose of the mail
#Reason can have the following values: OTP, new_registration, reminder 

class Send_Mail:

    def __init__(self, receiver, reason, **kwargs):

        self.receiver = receiver
        self.reason = reason
        self.kwargs = kwargs
        self.sender = "coderssvartak@gmail.com"
        self.pswd = "Vartak@213"
        self.sent = self.send()

    def send(self):

        if 'otp' in self.reason.lower():
            subject = "One Time Password sent by Password Generator"
            with open("One Time Password.txt", "r") as file:
                content = file.read()
                content += o.otp()
        
        #Integrate the user's username after once db is connected
        elif 'regist' in self.reason:
            subject = "Welcome user"
            with open("new_registration.txt", "r") as file:
                content = file.read()
            username = ''
            for key, value in self.kwargs.items():
                if 'username' in key.lower():
                    username = value
            content += username

        #Integrate the account name once db is connected
        elif 'remind' in self.reason:
            subject = "Reminder to change password"
            with open("reminder.txt", "r") as file:
                content = file.read()
            account_name = ''
            for key, value in self.kwargs.items():
                if 'account_name' in key.lower():
                    account_name = value
            content += account_name
        else:
            return False

        content += "\nNot you? You can ignore this mail or register a complaint at "+self.sender
        s = Server_Mail(self.sender, self.receiver, subject, content, self.pswd)
        flag = s.send_mail()
        return(flag)
        
        
"""
#Driver Code
#OTP
sent = Send_Mail("", "otp")

#Registration
sent = Send_Mail("", "register", username="")

#Reminder
sent = Send_Mail("", "register", account_name="")
"""
