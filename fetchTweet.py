#!/usr/bin/python
# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pymongo

''' Assumes a file ".keys.json" where all credentals are stored as:
[{
    "consumer_key": "",
    "consumer_secret": "",
    "access_token": "",
    "access_token_secret": ""
}]
'''

with open('.keys.json', 'r') as myFile:
    data = json.load(myFile)

consumer_key = data[0]['consumer_key']
consumer_secret = data[0]['consumer_secret']
access_token = data[0]['access_token']
access_token_secret = data[0]['access_token_secret']

# momngo connection
from pymongo import MongoClient

# client = MongoClient('mongodb://root:pass@ds013456.mlab.com', 13456)
# db = client['precog-summer']
# collection = db['samples']

client = MongoClient('localhost', 27017)
db = client['analysis']
collection = db['brexit']


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        print(type(data))
        collection.insert(json.loads(data))
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['brexit', 'theresamay', 'stopbrexit',
                         'brexitdeal','brexitshambles'
                         ])
