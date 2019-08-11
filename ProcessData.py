######################################################################################
# Project           : Twitter Sentiment Analyzer 
# Program name      : ProcessData.py 
# Author            : Aaron Almeida
# Date created      : 11/09/2019
# Purpose           : Processes the data downloaded using regular expressions 
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


#open the saved file of data and write it into a array of dictionaries 
def openFile():
     theList = []
     with open('test.csv', 'r') as csvfile:
          lineReader  = csv.reader(csvfile, delimiter =',', quotechar = "\"")
          for row in lineReader:
               #print(row)
               theList.append({"tweet_id": row[0], "text":row[1],"label":row[2], "topic":row[3]})
     return theList




# a class to process(clean) the tweets of uneeded stuff
class PreProcessTweets:
    
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER','URL'])
 
    def processTweets(self, list_of_tweets):
        processedTweets=[]
        for tweet in list_of_tweets:
            processedTweets.append((self._processTweet(tweet["text"]),tweet["label"]))
        return processedTweets
    
    def _processTweet(self, tweet):
        tweet = tweet.lower() # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet) # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # remove the # in #hashtag
        tweet = word_tokenize(tweet) # remove repeated characters (helloooooooo into hello)
        return [word for word in tweet if word not in self._stopwords]
          
