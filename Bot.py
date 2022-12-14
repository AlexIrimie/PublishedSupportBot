
import praw
import information
import os
import time
import csv
from datetime import datetime


#Bot information stored in information.py
client_id = information.client_id 
client_secret = information.client_secret
username = information.username 
password = information.password
user_agent = information.user_agent


#set up reddit with praw
reddit = praw.Reddit(client_id = client_id,  
                     client_secret = client_secret,  
                     username = username,  
                     password = password, 
                     user_agent = user_agent)


#get subreddit name
subreddit = reddit.subreddit(information.subreddit_name)






def startBot(subreddit, comments_replied_to):
    
    
    
    print("starting")
    updated_posts = []
    streamnumber = 0
    
    
    
    #My system for being able to get comment trees even if the comment is on an old post
    for comment in subreddit.stream.comments():
        streamnumber += 1
        
        if comment.id not in comments_replied_to:
            blank1, r, name, something, postID, postname, commentid, blank2 = comment.permalink.split("/")
            if postID not in updated_posts:
                updated_posts.append(postID)
        if streamnumber == 100:
            print("break")
            break
 
 
 #Start looking for comments to reply to
    for idnumber in updated_posts:
        submission = reddit.submission(idnumber)
        for comment in submission.comments:
            comment.refresh()
            
            for supportType in information.classes:
                if supportType.callsign in comment.body and comment.id not in comments_replied_to and comment.author != reddit.user.me():
                    #Make sure bot doesnt comment on same post twice
                    comments_replied_to.append(comment.id)
                    with open("IDS.txt", "a") as f:
                            f.write(comment.id + "\n")
                            
                    #Add information to timesRequested.csv
                    information.addtocsv(str(submission.author))
                    
                    #Add information to support File
                    information.addsupportdata(supportType.title)
                    
                    #Reply :: May want to change the message, this is just in place to mention the author the bot is replying to
                    comment.reply(body=f"Hello, {submission.author}, {supportType.message}")
                    
            #Same as code above but for replies
            for reply in comment.replies:
                
                for supportType in information.classes:
                    if supportType.callsign in reply.body and reply.id not in comments_replied_to and reply.author != reddit.user.me():
                        #Make sure bot doesnt comment on the same comment twice
                        comments_replied_to.append(reply.id)
                        with open("IDS.txt", "a") as f:
                            f.write(reply.id + "\n")
                        
                        #Add information to timesRequested.csv
                        information.addtocsv(str(comment.author))
                        
                        #Add information to support file
                        information.addsupportdata(supportType.title)
                        
                        #Reply
                        reply.reply(body=f"Hello, {comment.author}, {supportType.message}")
    updated_posts = []
    time.sleep(10)
    
    
    
    
    return



#Gets saved comments as to not reply to the same comment multiple times
def get_saved_comments():
    if not os.path.isfile("IDS.txt"):
        comments_replied_to = []
    else:
        with open("IDS.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))
    return comments_replied_to

comments_replied_to = get_saved_comments()


#Get the last date a post was made
def lastDate():
    if not os.path.isfile('datefile.txt'):
        date = datetime.now().strftime("%Y, %m, %d")
        with open('datefile.txt', 'w') as f:
            f.write(date)
            
    with open('datefile.txt', 'r') as f:
        date = f.read() 
            
    if not date:
        with open('datefile.txt', 'w') as f:
            f.write(datetime.now().strftime("%Y, %m, %d"))
            
            
    date = date.split(',')
    
            
    return date


#Define a day and self subreddit for self posts
ONEDAY = 86400
selfsubreddit = reddit.subreddit(f"u_{information.username}")


while True:

    #Updates the support types on every run to keep the bot dynamic
    information.makeclasses()
    startBot(subreddit, comments_replied_to)
    
    
    #! Delete Everything under this comment if you don't want bot to make self posts
    #Every increment of days, make a self post with support data.
    if (datetime.now() - datetime(int(lastDate()[0]), int(lastDate()[1]), int(lastDate()[2]))).total_seconds() > ONEDAY: #<---- 7*ONEDAY for a week
        print("Making Self Post")
        with open('datefile.txt', 'w') as f:
            f.write(datetime.now().strftime("%Y, %m, %d"))
        tempmessage = ""
        with open('supportData.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            csv_to_list = list(reader)
        for item in csv_to_list:
            tempmessage += f"{item[0]}, {item[1]}\n\n"
        
        print(tempmessage)
        selfsubreddit.submit(title = "Information", selftext = tempmessage)
    