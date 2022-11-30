
#! IMPORTANT: MAKE SURE IF CHANGING FILES NAMES TO EDIT THE CODE TO READ THE CORRECT FILE


import configparser
import csv

client_id = "" 
client_secret = "" 
username = "" 
password = "" 
user_agent = ""
    
    

#Can edit config file name here
#This is the file to add or remove support types
configfile = 'SupportConfig.INI'



config = configparser.ConfigParser()
config.read(configfile)

#Makes the support types into classes for the bot to use
def makeclasses():
    sections = config.sections()
    for section in sections:
        title = config[section]['title']
        message = config[section]['message']
        callsign = config[section]['callsign']
        new_class = makeone(message, callsign, title)
        classes.append(new_class)


#Used when a new user needs support
class user:
    def __init__(self, author, countrequested):
        self.author = author
        self.countrequested = countrequested
        
    
users = []



#When called, either adds the support type called to the file or adds one to the existing count
def addsupportdata(supporttype):
    
    
    #This is the file where the data on  how many times each support is called is displayed
    filename = 'supportData.csv'
    
    newrow = supporttype, 1
    
    #Make top row nice
    with open(filename, 'r+', newline='') as t:
        writer = csv.writer(t)
        if t.tell() == 0:
            writer.writerow(['Support Type', 'Times Requested'])
        t.close()
        
    #Add support type count if needed
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        supportList = list(reader)
        for item in supportList:
            if item[0] == supporttype:
                item[1] = int(item[1]) + 1
                f.close()
                with open(filename, 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(supportList)
                    f.close()
                    return
    #Add row if support type does not exist in the csv
    supportList.append(newrow)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(supportList)
    f.close()
    return


#When called, either adds a user to the desired file or adds one to the amount of times they called support
def addtocsv(user):
    
    
    #This is the file where the user data is stored
    filename = 'userData.csv'
    
    newrow = str(user), 1
    
    #Make top row nice
    with open(filename, 'r+', newline='') as t:
        writer = csv.writer(t)
        if t.tell() == 0:
            writer.writerow(['User', 'Times Requested'])
    t.close()
    
    #Add one to persons count if needed
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        csvlist = list(reader)
        for item in csvlist:
            if item[0] == user:
                item[1] = int(item[1]) + 1
                f.close()
                with open(filename, 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(csvlist)
                    f.close()
                    return
    #Add new row if the user isnt in the database
    csvlist.append(newrow)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csvlist)
    f.close()
    return
        

#Makes the support data from the config file into a class
class makeone:
    def __init__(self, message, callsign, title):
        
        self.title = title
        self.message = message
        self.callsign = callsign

classes = [
    
]



#Probably change this to 'RocketLeague' lol
subreddit_name = "bottesting"