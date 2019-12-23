import requests
import urllib3

url = 'https://api.pushshift.io/reddit/submission/search/?q=title&&field=body&subreddit=brogress'

response = requests.get(url)

data = response.json()

print(data)