#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Requirement:
# The mongod server must be running.
#
# ..
from collections import Counter
import pymongo
import re
from pymongo import MongoClient

# To import the collection to mongoDB:
# mongoimport -d analysis -c brexit  --file brexit.json

client = MongoClient('localhost', 27017)
db = client['analysis']
collection = db['brexit']

THERESA = re.compile('theresa|theresamay|maytheresa')

outfile = open('output_file.txt', 'w')
outfile.write('''
    ###############
    BREXIT ANALYSIS
    ###############
    ''')

def find_popularity():
    # ----------------------
    # Mentions of Theresa names: 153
    # Total tweets:  5000
    # -----------------------
    outfile.write("\nMentions of Theresa May:\n--------------")
    theresa = 0
    # db_max = 100000
    # db_min = 0
    total_valid = 0

    cursor = collection.find({})
    for doc in cursor:
        # db_min += 1
        # if db_min < db_max:
        try:
            text = doc['text']
            total_valid += 1
        except KeyError:
            # print doc['_id']
            pass
        # print text
        theresa += len(THERESA.findall(text.lower()))
        # else:
        #     break
    outfile.write("\nMentions of Theresa names:" + str(theresa))
    outfile.write("\nTotal tweets: " + str(total_valid))

    outfile.write('\n')


def top_20_hashtags():
    # -------------------
    # count hashtag
    # -------------------
    outfile.write("\nTop 20 hashtags:\n--------------\n")
    # 573 brexit
    # 36 eu
    # 32 revokearticle50
    # 27 indicativevotes
    # 26 brexitshambles
    # 24 wtobrexitnow
    # 23 peoplesvote
    # 21 brexitstorm
    # 15 nodeal
    # 14 nhs
    # 13 indicativevotes2
    # 12 theresamay
    # 12 singlemarket
    # 10 stopbrexit
    #  9 r4today
    #  9 twatinahat
    #  8 brexitbetrayal
    #  8 uk
    #  7 brexitchaos
    #  7 fbpc
    # -------------------
    # Also, total number of hashtags used: 1462
    '''
    Traverse through all hashtags in every tweet
    - hashtags are present in the attribute - entities.hashtags
    - return value - array of hashtags, empty is no hashtag
        {"indices":[x,y], "text": <hashtag-text-here>}

    To generate word cloud: https://www.wordclouds.com/
    '''
    cursor = collection.find({})
    # db_max = 10
    # db_min = 0
    hashtag_counter = Counter()
    for doc in cursor:
        # db_min += 1
        # if db_min < db_max:
        try:
            hashtag_list = doc['entities']['hashtags']
            if len(hashtag_list) > 0:
                for ht in hashtag_list:
                    hashtag_counter[ht['text'].lower()] += 1
        except KeyError:
            pass
        # else:
            # break
    top_20 = hashtag_counter.most_common(20)

    for word, count in top_20:
        outfile.write(word + ": " + str(count) + "\n")
    outfile.write("\nTotal number of hashtags used: " + str(sum(hashtag_counter.values())) + "\n")
    outfile.write('\n')


def original_vs_retweeted():

    outfile.write("\nTypes of tweets - original vs retweeted:\n--------------")
    # Original tweets don't have the attribute
    #   retweeted_status
    # Original
    # db.getCollection('brexit').find({"retweeted_status":{$eq:null}},{}).length()
    res = collection.count_documents({"retweeted_status":{'$eq':None}},{})
    outfile.write("\nNumber of original tweets: " + str(res))
    # 1424
    # Retweeted
    # db.getCollection('brexit').find({"retweeted_status":{$ne:null}},{}).length()
    res = collection.count_documents({"retweeted_status":{'$ne':None}},{})
    outfile.write("\nNumber of retweeted tweets: " + str(res))
    # 3576

    outfile.write('\n')


def fav_counts():
    # find no of tweets greater than a number - ex: 50,000 => Outputs: 3
    # raw mongo query
    # db.getCollection('brexit').find({'retweeted_status.favorite_count':{$gt:30000}}).length()
    outfile.write("\nCounts of the favorites on tweets:\n--------------")
    times = [1, 100, 1000, 5000, 10000, 50000]
    for value in times:
        res = collection.count_documents({'retweeted_status.favorite_count':{'$gt':value}})
        outfile.write("\nNumber of tweets favorited more than" + str(value) + "times: " + str(res))

    # some queries:
    # gt  50,000 : 3
    # gt  10,000 : 108
    # gt    5000 : 187
    # gt    1000 : 861
    # gt     100 : 1896
    # gt       1 : 3295

    outfile.write('\n')


def tweet_type():

    outfile.write("\nTypes of tweet content - text vs audio vs video\n--------------")
    # only text: 4822
    # db.getCollection('brexit').find({'entities.media.type':{$eq:null}}).length()
    res = collection.count_documents({'entities.media.type':{'$eq':None}})
    outfile.write('\nTweets with only text: ' + str(res))
    # ----
    # contains Photo: 178
    # db.getCollection('brexit').find({'extended_entities.media.type':'photo'}).length()
    res = collection.count_documents({'extended_entities.media.type':'photo'})
    outfile.write('\nTweets with images: ' + str(res))
    # ----
    # contains Video: 19
    # db.getCollection('brexit').find({'extended_entities.media.type':'video'}).length()
    res = collection.count_documents({'extended_entities.media.type':'video'})
    outfile.write('\nTweets with videos: ' + str(res))
    # ----

    outfile.write('')


def main():
    find_popularity()
    top_20_hashtags()
    original_vs_retweeted()
    fav_counts()
    tweet_type()

if __name__ == '__main__':
    main()
