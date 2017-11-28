import tweepy
import json
import time

consumer_key = 'z4OMjR0lY1PGYojysSZK4bLtf'
consumer_secret = 'aBBWdQK1aT4mKLIz2zbD42fLJJhQUaKqfQkUSAkEEwxcKPDWlk'

access_token = '74024384-WGOxmxPOaAApRFLTvhETyqcoXErZ7Gn2021rjtnwG'
access_token_secret = '3N5JEE32n9GcQJhqps8VbzONNVHvWYHWYcwZOqnrPnyaU'

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
search_string = "ivanka trump visits india"

#public_tweets = api.search(search_string)

"""for tweet in public_tweets:
    print(tweet.text)
    analysis = (tweet.text)
"""
for status in tweepy.Cursor(api.search, q=search_string).items(20000):
    tweet = status._json
    ts = time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').tm_mday
    if ts == new_date:
        
