from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pandas.compat import u
import credentials
import numpy as np
import pandas as pd
import sys

if sys.version_info[0] >= 3:
    unicode = str

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        authorise = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
        authorise.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
        return authorise

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    # Class for streaming and processing live tweets.
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, fetched_tweets_filename, username):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        author = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(author, listener)
        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=username)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error= %s" % str(e))
        return True
          
    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer():
    def tweets_to_data_frame(self, tweets):
        data_frame = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        data_frame['len'] = np.array([len(tweet.text) for tweet in tweets])
        data_frame['date'] = np.array([tweet.created_at for tweet in tweets])
        data_frame['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        data_frame['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return data_frame

def split_into_tokens(message):
  message = unicode(message, 'utf8')  # convert bytes into proper unicode
  return TextBlob(message).words

if __name__ == '__main__':
    twitter_client = TwitterClient()        #creating objects of classes
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    
    if len(sys.argv) == 1:
        string_username = "KapilSharmaK9"   #specify the username
    else:
        string_username = sys.argv[1]
    
    tweets = api.user_timeline(screen_name=string_username, count=10) #get 10 tweets
    # Step 1: save these tweets to a .txt file
    file = open("tweets.txt", "w")
    tweets_text=[tweet.text.encode('utf-8','ignore') for tweet in tweets]
    
    for tweet in tweets_text:
        file.write(str(tweet) + "\n\n")
    file.close()

    # Step 2: save important info for these tweets to a .csv file
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df.to_csv(r'.\tweetsImportantInfo.csv')
    print(df.head(10))    