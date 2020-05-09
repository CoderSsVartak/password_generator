import random
import re

class Security_question:

    #Read the questions
    def read_qns():
        with open("security_qns.txt", "r") as file:
            data = file.read()
        file.close()

        data = random.shuffle(data)
        return data 

    #Checks to be performed before answers are stored
    def validation(self, answer):

        if "\\" in answer:
            return("Backslash present. Please remove the backslash")

        sym, word = bool(re.search(r"[@' \"|]", answer)), bool(re.search(r'[a-zA-Z0-9]', answer))
        temp = [not sym, word]
        return all(temp)


