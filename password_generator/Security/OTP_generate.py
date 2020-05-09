import random, string

def otp():

    temp = []
    for _ in range(6):
        temp.append(str(random.choice(string.digits)))
    
    return ''.join(temp)

