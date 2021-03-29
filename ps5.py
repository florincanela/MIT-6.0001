# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

    

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        text = text.lower()

        # spliting the text at char and rejoining -  for every punctuation char
        for char in string.punctuation: #O(1)
            if char in text:  #O(n)
                text = text.split(char)
                text = " ".join(text)                       

        # spliting phrase and text for iteration for every word
        polished_phrase = text.split()
        phrase = self.phrase.split()

        # setting a flag 
        flag = 0
        #for every word in text
        for i in range(len(polished_phrase)):
            # if that word matches first phrase word
            if polished_phrase[i] == phrase[0]:
                # check if the following word/words in phrase match
                #  following words/word in txt
                for j in range(len(phrase)):
                    try:
                        if polished_phrase[i+j] != phrase[j]:
                            # if it does not, reset the flag and break out of the inner
                            #  loop(which loops through all words in phrase)                         
                            flag = 0
                            break
                        else:
                            # if word matches add a match point to flag // if flag has
                            #  matches for evey word in phrase return true
                            flag +=1
                            if flag == len(phrase):
                                return True
                    except IndexError:
                        # if the first word in phrase is the last word in text the inner 
                        # loop will attempt to check the next word of the text against
                        #  next of phrase thus IndexError occoring
                        return False      
        return False
        
                    




# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())
    


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S")


# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        try:
            condition = self.time > story.get_pubdate()
        except:
            condition = self.time.replace(tzinfo=pytz.timezone("EST")) > story.get_pubdate()

        return condition



class AfterTrigger(TimeTrigger):
    def evaluate(self, story):

        #tests compare our time against offset aware(timezone) and offset-naive separately
        try:
            #first we try offset naive - no timezone
            condition = self.time < story.get_pubdate()
        except:
            # if EXCEPTION - we set our timezone to EST - offset aware
            condition = self.time.replace(tzinfo=pytz.timezone("EST")) < story.get_pubdate()

        return condition

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger  = trigger
    
    def evaluate(self, news_item):
        return not self.trigger.evaluate(news_item)


# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, news_item):
        return self.trigger1.evaluate(news_item) and self.trigger2.evaluate(news_item)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, news_item):
        return self.trigger1.evaluate(news_item) or self.trigger2.evaluate(news_item)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)

    triggered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggered_stories.append(story)
                break
        
    return triggered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    # dictionary of objects/triggers instantianted from the classes below
    trigger_dict = {}

    #dictionary of classes
    class_dict = {
        "TITLE" : TitleTrigger,
        "DESCRIPTION" : DescriptionTrigger,
        "AFTER" : AfterTrigger,
        "BEFORE" : BeforeTrigger,
        "NOT" : NotTrigger,
        "AND" : AndTrigger,
        "OR" : OrTrigger
    }

    res = []
    #for every line in triggers list
    for trigger in lines:
        trigger = trigger.split(",")
        #check if starts with "ADD"
        if trigger[0] == "ADD":
            # adds to list the specified objects/triggers
            for obj in trigger[1:]:
                res.append(trigger_dict[obj])
            # and breaks the loop because ADD is last line    
            break
        #check if is an OR or AND trigger
        if trigger[1] == "OR" or trigger[1] == "AND":
            # adds to dictionary of objects an object instantianted with objects from the same dictionary
            trigger_dict[trigger[0]] = class_dict[trigger[1]](trigger_dict[trigger[2]], trigger_dict[trigger[3]])

        else:
            #instantiantes the object using the object dict with phrase(being at index 2)
            trigger_dict[trigger[0]] = class_dict[trigger[1]](trigger[2])

    return res
    


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Covid")
        t2 = DescriptionTrigger("Hospitals")
        t3 = DescriptionTrigger("Vaccine")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()


