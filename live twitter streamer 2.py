from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API 
from tweepy import Cursor
 
import twitter_credentials
import numpy as np
import pandas as pd
import csv
 
# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, retrieved_tweets_filename, tweet_subject):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(retrieved_tweets_filename)
        auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
        auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_token_secret)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=tweet_subject)


# # # # TWITTER STREAM LISTENER # # # #       
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, retrieved_tweets_filename):
        self.retrieved_tweets_filename = retrieved_tweets_filename
    
    tweets=[]
    
    def on_data(self, data):
        tweetdata = []
        try:
            #print(data)
            with open(self.retrieved_tweets_filename, 'a') as tf:
                tf.write(data)        
                tweetdata += data
            tweets.append(tweetdata)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
        
        print(tweets)
    
    def on_error(self, status):
        print(status)
          
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])                                                   #loop to extract text from tweet list and add heading tweets.. Is this correct?
        #df['id'] = np.array([tweet.id for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets], columns=['Date'])
        df['source'] = np.array([tweet.source for tweet in tweets], columns=['Twitter Handle'])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets], columns=['Number of likes'])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets], columns=['Number of reweets'])
        df['len'] = np.array([len(tweet.text) for tweet in tweets], columns=['Character length'])

        return df

 
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    tweet_subject = ["$TSLA", "Elon Musk"]
    retrievedd_tweets_filename = "Tesla_tweets.csv"
    
    tweets = StdOutListener.tweets

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(retrievedd_tweets_filename, tweet_subject)
    
    
    tweet_analyzer = TweetAnalyzer()
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    print(df.head(10))
    
  



#https://www.youtube.com/watch?v=wlnx-7cm4Gg&t=430s