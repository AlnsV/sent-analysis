import tweepy
import json
import time




class TwitterAnalizer():

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, *args, **kwargs):

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(self.auth)
        self.check = True

        for status in tweepy.Cursor(self.api.search, q=search_string).items(20000):
            tweet = status._json
            ts = time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').tm_mday
            print(tweet,ts)




if __name__ == "__main__":

    consumer_key = 'z4OMjR0lY1PGYojysSZK4bLtf'
    consumer_secret = 'aBBWdQK1aT4mKLIz2zbD42fLJJhQUaKqfQkUSAkEEwxcKPDWlk'

    access_token = '74024384-WGOxmxPOaAApRFLTvhETyqcoXErZ7Gn2021rjtnwG'
    access_token_secret = '3N5JEE32n9GcQJhqps8VbzONNVHvWYHWYcwZOqnrPnyaU'

    search_string = "ivanka trump visit india"

    Tw = TwitterAnalizer(consumer_key, consumer_secret, access_token, access_token_secret, search_string)
