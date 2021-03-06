##############
# Connect to the Twitter API and collect latest 7 days of tweets.
##############
# Libraries
import csv,json,simplejson,tweepy
from datetime import date, timedelta

# Twitter credentials
consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''

# Connect to API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True) # Will pause the output until rate limit refreshes, this is normal
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Get current date to define filenames
today = date.today()
last_week = today - timedelta(days=7)
print(today, last_week)

# Check current date file doesn't already exist
in_use = False
try:
    check = open(str(today) + "_" + str(last_week) + ".json","r")
    print("File already exists. Please change name or delete if appropriate.") # May need to restart IPython console 
    in_use = True
except:
    if in_use == False:
        print("Creating output file.")
        output_file = open(str(today) + "_" + str(last_week) + ".json","w")
    
tweets = []
count = 0    

# If there are no clashes, contact the Search API with the following parameters
if in_use == False:
    for tweet in tweepy.Cursor(api.search,
                               q="query", 
                               count=100,
                               result_type="recent",
                               include_entities=True,
                               tweet_mode="extended", #This is needed to return tweets > 140 characters
                               geocode=('54.06835,-2.86108,1000mi') # Change this to modify location data
                               ).items():
        print(tweet.created_at, tweet.full_text)
        count += 1
        print("***")
        tweet_j = tweet._json
        tweets.append(tweet_j)
        
    print("Writing tweets to file - takes a while...")
    simplejson.dump(tweets,output_file)
    print("Tweets between " + str(last_week) + " and " + str(today) + ": " + str(count))
output_file.close()