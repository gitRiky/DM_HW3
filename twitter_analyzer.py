#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import codecs
import json
from httplib import IncompleteRead
import time

TWEET_COUNT = 1000000

# Variables that contains the user credentials to access Twitter API
input_file = file("API twitter.txt", 'r')
consumer_key = input_file.readline().replace("\n", "").replace("\r", "")
consumer_secret = input_file.readline().replace("\n", "").replace("\r", "")
access_token = input_file.readline().replace("\n", "").replace("\r", "")
access_token_secret = input_file.readline().replace("\n", "").replace("\r", "")
input_file.close()
counter = TWEET_COUNT

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    counter = TWEET_COUNT

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            if json_data.has_key("entities"):
                if json_data["entities"].has_key("hashtags"):
                    for hashtag in json_data["entities"]["hashtags"]:
                        file_handle.write(hashtag["text"])
                        file_handle.write("\n")
            #print hashtags
            StdOutListener.counter -= 1
            if StdOutListener.counter == 0:
                return False
        except IncompleteRead:
            print "I.R"
            return True
        return True

    def on_error(self, status):
        return True


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    with codecs.open("twitter_stream2.txt", "w", encoding="utf-8") as file_handle:
        while True:
            try:
                stream.sample()
            except:
                print "I.R."
                continue


    # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # stream.filter(track=['nba', "soccer", "football", "tennis", "motogp", "basket", "volleyball"])
