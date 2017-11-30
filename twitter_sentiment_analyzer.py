import tweepy
import time
import datetime as dt
import re

from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.gridspec as gridspec


def percentages(x, pos):
    return '%0.0f %%' % (x * 100)


class TwitterAnalizer():

    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_secret, waiting_mode=False, *args, **kwargs):

        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(self.auth, wait_on_rate_limit=waiting_mode) if waiting_mode else tweepy.API(self.auth)
        self.day = dt.datetime.now().weekday()
        self.day_lists = [[],[],[],[],[],[],[]]   #self.day_distribution()
        #self.wdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        self.stop_words = set(stopwords.words("english"))

        self.waiting_mode = waiting_mode

    def analyze_sentiment(self):
        sia = SIA()

        # Creating scores dataframe.
        columns = ['Positives', 'Neutral', 'Negatives']
        scores = pd.DataFrame(columns=columns)

        # Looping through the tweets lists.
        for i in range(7):
            positives = 0
            negatives = 0
            neutral = 0
            # Looping through the tweets.
            for tweet in Tweets_lists[i]:
                score = sia.polarity_scores(tweet)
                if score['compound'] > 0.10:
                    positives += 1
                elif score['compound'] < -0.10:
                    negatives += 1
                else:
                    neutral += 1

            # Populating the database.
            day = dt.date.today() - dt.timedelta(days=6 - i)
            scores.at[day, :] = [int(positives), int(neutral), int(negatives)]

        # Creating scores percentage dataframe.
        scores_pct = pd.DataFrame(columns=columns)
        for column in columns:
            scores_pct[column] = scores[column] / scores.sum(axis=1)
        scores_pct.fillna(0, inplace=True)

        self.scores = scores
        self.scores_pct = scores_pct

        return scores, scores_pct


    def search_feed(self, search_words):
        #iterating through the tweets in order to assing them to a list wich represents the day created of the tweet.
        if self.waiting_mode:
            tw_cursor = tweepy.Cursor(self.api.search, q=search_words, lang='en').pages()
        else:
            tw_cursor = tweepy.Cursor(self.api.search, q=search_words, lang='en').pages(50)

        print('\nSearching for tweets')
        for page in tw_cursor:
            for status in page:
                tweet = status._json
                ts = dt.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').weekday()

                tweet_text = self.clean_content(tweet['text'])
                tweet_text = self.pre_process(tweet_text)
                self.day_lists[ts].append(tweet_text)

        # Sorting lists.
        today = dt.date.today().weekday()
        self.day_lists = self.day_lists[today + 1:] + self.day_lists[0 : today + 1]

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

    def limit_handled(self, cursor):
         while True:
             try:
                 yield cursor.next()
             except tweepy.error.TweepError:
                 print('\nWaiting until the Twitter API allows us to search more tweets...')
                 time.sleep(15 * 60)



if __name__ == "__main__":
    # User variables.
    search_string = "ethereum"
    waiting_mode = False

    consumer_key = 'z4OMjR0lY1PGYojysSZK4bLtf'
    consumer_secret = 'aBBWdQK1aT4mKLIz2zbD42fLJJhQUaKqfQkUSAkEEwxcKPDWlk'
    access_token = '74024384-WGOxmxPOaAApRFLTvhETyqcoXErZ7Gn2021rjtnwG'
    access_token_secret = '3N5JEE32n9GcQJhqps8VbzONNVHvWYHWYcwZOqnrPnyaU'

    # Analyzing tweets.
    Tw = TwitterAnalizer(consumer_key, consumer_secret, access_token,
                         access_token_secret,
                         waiting_mode=waiting_mode)
    Tweets_lists = Tw.search_feed(search_string)
    print("\nAnalyzing the sentiment of the tweets")
    scores, scores_pct = Tw.analyze_sentiment()

    # Making plots
    print("\nCreating charts")
    gs = gridspec.GridSpec(5, 5,
                       width_ratios=[2, 14, 3, 14, 2],
                       height_ratios=[1, 2, 1, 8, 1],
                       wspace=0, hspace=0
                       )

    ax1 = plt.subplot(gs[6:10])
    ax2 = plt.subplot(gs[16:17])
    ax3 = plt.subplot(gs[18:19])
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10)

    ax1.text(0.01, 0.5,
             "Sentiment analysis of the search:\n '" + search_string + "'",
             fontdict={'fontname':'DejaVu Sans'},
             color='#6194BC',
             fontsize=29)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.tick_params(axis=u'both', which=u'both',length=0)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)

    ax2 = scores.plot(ax=ax2, kind='bar', color=['#A5D1F3', '#E4001B', '#E49D67'])
    ax2.set_title('Number of tweets', fontsize=22)
    for tick in ax2.get_xticklabels():
        tick.set_rotation(45)

    ax3 = scores_pct[['Positives', 'Negatives']].plot(kind='bar',
                                                      color=['#A5D1F3', '#E4001B'],
                                                      ax=ax3)
    ax3.set_title('Percentage of positive and negative tweets',
                  fontsize=22)
    for tick in ax3.get_xticklabels():
        tick.set_rotation(45)
    formatter = FuncFormatter(percentages)
    ax3.yaxis.set_major_formatter(formatter)

    fig.savefig(search_string + '.png')
