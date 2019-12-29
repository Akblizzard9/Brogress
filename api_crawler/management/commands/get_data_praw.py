import praw
import re
import json
import unicodedata
import os
import psycopg2
import psycopg2.extras


####BEFORE RUNNING THIS SCRIPT MAKE SURE YOUR DB IS SET UP BY RUNNING 'python manage.py migrate' FROM /brogress_backend####
DATABASE_URL = os.environ['DATABASE_URL']

#establishes connection to our database
conn=psycopg2.connect(DATABASE_URL)
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

#Praw is a wrapper for reddit's api, use it, life gets easier, 
# these are the credentials, hide them when we push to production
reddit = praw.Reddit(client_id = '', \
                     client_secret = '', \
                     user_agent = '', \
                     username = '', \
                     password = '' )

#selection of subreddit
subreddit = reddit.subreddit('brogress')
#this will allow us to loop through new post, limit=how many youd like to loop through, max:1000 
#PRAW only allows the newest 1000 post to be pulled, we will work on using pushshift.io to pull older posts
top_subreddit = subreddit.new(limit=999)



topics_list = []

#feel free to clean up the regex, works about on 90% but older post with less structure produce more errors. 

for submission in top_subreddit:
    print(submission.title)

    #unique post id that can be used to delete duplicate posts from database
    submission_id = submission.id

    #this is the url for the photo posted
    submission_url = submission.url

    #gets the sex of the poster
    sex = re.search('[M|F]', submission.title)
    if sex is not None:
        sex = sex.group()
            
            
    #gets the age of the poster
    age = re.search(r'\b\d{2}\b', submission.title)
    if age is not None:
        age = age.group()
    

    #gets height of the poster
    height = re.search(r'(?i)(?<=\/\d\d\/)((\d)(\d)(\d)..|(\d.\d.))' , submission.title)
    if height is not None:
        height = height.group()
        print(height)
        numberonly = re.findall(r'\d+', height)
        if len(numberonly) == 1:
                baseUnit = str(numberonly[0]) + 'cm'
                
        if len(numberonly) == 2:  
            firstdigit = numberonly[0]
            seconddigit = numberonly[1]
            baseUnit = str(int(firstdigit) * 12 + int(seconddigit)) + 'in'
            
    
        

    #gets starting weight
    startweight = re.search(r'(?i)((\d+)kg)|((\d+)lbs)',submission.title)
    if startweight is not None:
        startweight = startweight.group()
   

    #gets ending weight
    endweight = re.search(r'(?i)(?<= to )(\d+)lbs|(\d+)kg',submission.title)
    if endweight is not None:
        endweight = endweight.group()
    
    #gets timeframe from post
    timeframe = re.search(r'\((.*?)\)',submission.title)
    if timeframe is not None:
        timeframe = timeframe.group(1)
    
    #data pulled appended to list to be inserted into db
    topics_list.append(( submission_id, sex, baseUnit, startweight, endweight, timeframe, age, submission_url))

#inserts all data pulled into database
for post in topics_list:
    query = ("INSERT INTO api_crawler_apidata (post_id, sex, height, start_weight, end_weight, total_time, age, image_sources) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    
dict_cur.executemany(query, topics_list)
conn.commit()
print(query)
    



