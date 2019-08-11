######################################################################################
# Project           : Twitter Sentiment Analyzer 
# Program name      : CollectData.py 
# Author            : Aaron Almeida
# Date created      : 11/09/2019
# Purpose           : Collect the data from twitters database
# Revision History  : Version 1
####################################################################################


import twitter
import csv
import time
import re
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords 

#initialize api 


#Can't disclose my keys to everyone ;) 
twitter_api = twitter.Api(consumer_key = 'Get from twitters API Tool!',
                         consumer_secret = 'Get from twitters API Tool!',
                         access_token_key = 'Get from twitters API Tool!',
                         access_token_secret = 'Get from twitters API Tool!')


#print(testDataSet[0:4])

#extract tweets from twitters database, uses the corpus file for refrence to tweet id (process takes 10 hours)
def buildTrainingSet(corpusFile, tweetDataFile):
     corpus = []

     #open data saved in csv file 
     with open(corpusFile, 'r') as csvfile:
          lineReader  = csv.reader(csvfile, delimiter =',', quotechar = "\"")
          for row in lineReader:
               corpus.append({"tweet_id": row[2], "label":row[1],"topic":row[0]})

          #limit the amount of requests to make sure we dont go over the pull limit 
          rate_limit = 180
          sleep_time = 900/rate_limit

          trainingDataSet = []

          #add the tweet to the array of dictionaries
          for tweet in corpus:
               try:
                    status = twitter_api.GetStatus(tweet["tweet_id"])
                    print("New tweet has been fetched: " + status.text)
                    tweet["text"] = status.text
                    print(tweet)
                    trainingDataSet.append(tweet)
                    time.sleep(sleep_time)
               except:
                    continue
          #save data into a new file 
          with open(tweetDataFile, 'w') as csvfile:
               linewriter = csv.writer(csvfile,delimiter = ',',quotechar = "\"")
               for tweet in trainingDataSet:
                    try:
                         linewriter.writerow([tweet["tweet_id"],tweet["text"],tweet["label"],tweet["topic"]])
                    except Exception as e:
                         print(e)
          return trainingDataSet





