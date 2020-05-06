import random, string

class Random_Password:

    def __init__(self, length):

        self.length = length
        self.characters = string.ascii_letters + string.digits + "!#$%&()*+<_>?:;<=>/@[]^_{}~`"
        self.password = self.generate_password()

    #Generate the password by using random method.
    def generate_password(self):

        pw = str()
    
        #Choose one from each upper case, lower case, number and a special symbol
        pw = pw + (random.choice(string.ascii_uppercase)) + (random.choice(string.ascii_lowercase)) + (
            random.choice(string.digits)) + (random.choice("!#$%&()*+<_>?:;<=>/@[]^_{}~`"))

        for i in range(self.length-4):
            pw = pw + random.choice(self.characters)
        pw = ''.join(random.sample(pw, len(pw)))            #again shuffles the characters of the password
        
        return pw

"""
#Driver Code
length = 12         #Minimum Length is 6
r = Random_Password(length)
print(r.password)
"""
