import re
import json
import unicodedata
import os
import psycopg2
import psycopg2.extras


####BEFORE RUNNING THIS SCRIPT MAKE SURE YOUR DB IS SET UP BY RUNNING 'python manage.py migrate' FROM /brogress_backend####


#establishes connection to our database
conn=psycopg2.connect(
    database="brogress",
    user="",
    host="localhost",
    password=""
)
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


query = ("SELECT height FROM api_crawler_apidata; ")
    
dict_cur.execute(query)
conn.commit()


heights = dict_cur.fetchall()


for height in heights:
    for numbers in height:
        if numbers == None:
            print('null found')
        if numbers is not None:
            numberonly = re.findall(r'\d+', numbers)
            print(numberonly)
            if len(numberonly) == 1:
                heightinCM = numberonly
                print(heightinCM)
            if len(numberonly) == 2:  
                firstdigit = numberonly[0]
                seconddigit = numberonly[1]
                heightInInches = int(firstdigit) * 12 + int(seconddigit)
                print(str(heightInInches))