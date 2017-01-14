import utility
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import codecs
import json
import numpy
import config


TWEET_COUNT = 1000


# hash the line element, verify if at least one of them has a new max_tail
# if yes, then update the max_tail and execute a new estimation, otherwise
# return an empty list
def update_f0(line, max_tail, hash_functions):
    index = 0
    update = False
    for hash_function in hash_functions:
        h_elem = hash_function(line)
        if h_elem != '0' * config.HEX_LEN:
            tail = utility.get_least_sign_bit(h_elem)
            if tail > max_tail[index]:
                max_tail[index] = tail
                update = True
        index += 1
    estimation = []
    if update:
        for tail in max_tail:
            estimation.append(2 ** tail)
    return estimation


def compute_average(estimations, size):
    averages = []
    sum = 0
    counter = 0
    for estimation in estimations:
        sum += estimation
        counter += 1
        if counter == size:
            averages.append(sum / counter)
            sum = 0
            counter = 0
    return averages


def update_f2(line, z, hash_functions):
    for i in range(0, config.NUM_HASH_FAMILIES):
        z[i] += utility.my_hash(hash_functions[i](line))
    estimates = []
    for elem in z:
        estimates.append(elem ** 2)
    return int(numpy.average(estimates))


def main():
    # sample with twitter, into the on_data method will be called this function.
    hash_functions = utility.init_hash_families(config.NUM_HASH_FAMILIES)
    # Variables that contains the user credentials to access Twitter API
    input_file = file("API twitter.txt", 'r')
    consumer_key = input_file.readline().replace("\n", "").replace("\r", "")
    consumer_secret = input_file.readline().replace("\n", "").replace("\r", "")
    access_token = input_file.readline().replace("\n", "").replace("\r", "")
    access_token_secret = input_file.readline().replace("\n", "").replace("\r", "")
    input_file.close()

    # This is the listener which selects hashtags and print them into a file
    # After that, it computes the new max_tail and, if it changes, then
    # compute a new estimation, otherwise not
    class StdOutListener(StreamListener):
        f0 = 0
        counter = 0
        total_counter = 0

        def on_data(self, data):
            json_data = json.loads(data)
            # filter the tweets with hashtags
            if json_data.has_key("entities"):
                if json_data["entities"].has_key("hashtags"):
                    StdOutListener.counter += 1
                    for hashtag in json_data["entities"]["hashtags"]:
                        # write hashtag into the output file
                        StdOutListener.total_counter += 1
                        value = hashtag['text']
                        file_handle.write(value)
                        file_handle.write("\n")
                        # compute the new max_tail
                        new_est = update_f0(value, max_tail, hash_functions)
                        if len(new_est) > 0:     # it means that the estimation has been changed
                            StdOutListener.f0 = int(numpy.median(compute_average(new_est, config.GROUP_SIZE)))
                        # compute new f2
                        new_f2 = update_f2(value, z, hash_functions)
                        # print f0 and f2
                        print "Number of hashtags that have been seen =", StdOutListener.total_counter
                        print "Estimated f0 =", StdOutListener.f0
                        print "Estimated f2 =", new_f2
                        print
            if StdOutListener.counter == TWEET_COUNT:
                StdOutListener.counter = 0
                if raw_input("We analyzed " + TWEET_COUNT + " tweets, do you want to continue? y or n\n") == "n":
                    proceed.change()
                    return False
            return True

        def on_error(self, status):
            print status
            return True

    # This handles Twitter authentication and the connection to Twitter Streaming API
    proceed = utility.proceed()
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    # initialize both max_tail and z
    max_tail = [0] * config.NUM_HASH_FAMILIES
    z = [0] * config.NUM_HASH_FAMILIES
    with codecs.open("live.txt", "w", encoding='utf-8') as file_handle:
        while proceed.get_c() != "n":
            try:
                stream.sample()
            except:
                continue

main()
