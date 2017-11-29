import tweepy
import json
import datetime as dt
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

class TwitterAnalizer():

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, *args, **kwargs):

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(self.auth)
        self.day = dt.datetime.now().weekday()
        self.day_lists = [[],[],[],[],[],[],[]]   #self.day_distribution()
        #self.wdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        self.stop_words = set(stopwords.words("english"))


    def search_feed(self, search_words):
        #iterating through the tweets in order to assing them to a list wich represents the day created of the tweet.
        tw_cursor = tweepy.Cursor(self.api.search, q=search_words, lang='en').pages(60)


        for page in tw_cursor:
            for status in page:
                tweet = status._json
                ts = dt.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').weekday()

                tweet_text = self.clean_content(tweet['text'])
                tweet_text = self.pre_process(tweet_text)
                self.day_lists[ts].append(tweet_text)

        return self.day_lists

    def clean_content(self, tweet):

        """ replace URLS, @username, special chars, white spaces, hashtags, etc """
        tweet = tweet.lower()
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
        tweet = re.sub('@[^\s]+','',tweet)
        tweet = re.sub('[\s]+', ' ', tweet)
        tweet = re.sub('[\n]+', ' ', tweet)
        tweet = re.sub(r'[^\w]', ' ', tweet)
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        tweet = re.sub('rt','',tweet)
        tweet = tweet.replace(':)','')
        tweet = tweet.replace(':(','')
        tweet = tweet.strip('\'"')

        return tweet
    #preprocessing deleting stopwords the doing stemming
    def pre_process(self,tweet):
        snow_s = SnowballStemmer("english")
        token_word = word_tokenize(tweet)
        tokenized = []
        for word in token_word:
            if word not in self.stop_words:
                tokenized.append(snow_s.stem(word))

        return " ".join(tokenized)


if __name__ == "__main__":
    """
    consumer_key = 'z4OMjR0lY1PGYojysSZK4bLtf'
    consumer_secret = 'aBBWdQK1aT4mKLIz2zbD42fLJJhQUaKqfQkUSAkEEwxcKPDWlk'

    access_token = '74024384-WGOxmxPOaAApRFLTvhETyqcoXErZ7Gn2021rjtnwG'
    access_token_secret = '3N5JEE32n9GcQJhqps8VbzONNVHvWYHWYcwZOqnrPnyaU'
    """
    consumer_key = "6dALRQC3cXCVGFipRs9qXa5FX"
    consumer_secret = "y5uxugsNFJLhKgRy1tUC7RCkBjGbhfNUKjeEUMEjYaVEbkjSKB"
    access_token = "753293686805557252-yoT7aLzYBytVVl4wxYMIDQX5XvFDDaT"
    access_token_secret = "QZHJhvQ3ywFXGX2ZSRfupmhoVjD4r6XWN7Srzp3nRVBLd"

    search_string = "ivanka trump visits india"

    Tw = TwitterAnalizer(consumer_key, consumer_secret, access_token, access_token_secret)

    Tweets_lists = Tw.search_feed(search_string)
    print(Tweets_lists)
