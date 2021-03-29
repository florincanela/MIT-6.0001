if 0 or 1 and 0:
    print(True)
import string

# print(string.punctuation)


punctuation = string.punctuation

# phrase = []
# for char in punctuation:
#     if char in text:
#         text = text.split(char)               
#         break

# for word in text:
#     if word:
#         phrase.append(word.strip(punctuation + ' '))


# phrase = ' '.join(phrase)
# phrase = phrase.split(" ")
# phrase_trigger = phrase_trigger.split()

# flag = True

# for i in range(len(phrase)): 
#     if phrase[i] == phrase_trigger[0]:
#         for j in range(len(phrase_trigger)):
#             if phrase[i+j] != phrase_trigger[j]:
#                 flag = False



class PhraseTrigger():
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        text = text.lower()

        for char in string.punctuation:
            if char in text:
                text = text.split(char)
                text = " ".join(text) 
                print(text) 
                
        polished_phrase = text.split()
        phrase = self.phrase.split()
        print(polished_phrase)

        flag = 0
        for i in range(len(polished_phrase)):
            if polished_phrase[i] == phrase[0]:
                for j in range(len(phrase)):
                    try:
                        print("expected:", phrase[j],  "|||  Got:" ,polished_phrase[i+j])
                        if polished_phrase[i+j] != phrase[j]:                         
                            flag = 0
                            break
                        else:
                            flag +=1
                            if flag == len(phrase):
                                return True
                    except IndexError:
                        return False      
        return False
        






# text =   'The purple cow is soft and cuddly.'


# phrase_trigger = "purple cow"

# trigger_object = PhraseTrigger(phrase_trigger)
# print(trigger_object.is_phrase_in(text))

import datetime
import pytz


x = "31 Oct 2016 17:00:10"
time_old = datetime.datetime.strptime(x, "%d %b %Y %H:%M:%S")

print(time_old)
time_now = datetime.datetime.now()
print(time_now.astimezone(pytz.timezone("EST")))



