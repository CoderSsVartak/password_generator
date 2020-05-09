import smtplib
from email.message import EmailMessage

class Server_Mail:

    def __init__(self, sender, receiver, subject, content, sender_password):

        self.sender = sender
        self.sender_password = sender_password
        self.receiver = receiver
        self.subject = subject
        self.content = content
        self.SMTPServer = 'smtp.gmail.com'
        self.port = 465 
        self.msg, self.server = self.initialize()

    def initialize(self):

        msg = EmailMessage()
        server = smtplib.SMTP_SSL(self.SMTPServer, self.port)
        return msg, server
    
    def send_mail(self):

        self.msg.set_content(self.content)
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        try:
            try:
                self.server.login(self.sender, self.sender_password)
            except smtplib.SMTPAuthenticationError:
                return("Invalid Username or Password or unknown receiver")

            self.server.send_message(self.msg)
            self.server.quit()
            return("Mail Sent")

        except smtplib.SMTPAuthenticationError:
            return("Authentication Error occurred.Retry again")
        except ConnectionRefusedError:
            return("Connection Refused by the sever")
        except smtplib.SMTPNotSupportedError:
            return("Server does not Support SMTP")

"""
#Driver Code
fromaddr = ''
password = ''
toaddrs = ''
subject = "Test Mail2"
content = "This is a server sent mail."
mail = Server_Mail(fromaddr, toaddrs, subject, content, password)
report = mail.send_mail()
print(report)
"""
