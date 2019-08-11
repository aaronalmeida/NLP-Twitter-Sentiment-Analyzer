######################################################################################
# Project           : Twitter Sentiment Analyzer 
# Program name      : SentAnalysis.py 
# Author            : Aaron Almeida
# Date created      : 11/09/2019
# Purpose           : Uses a corpus to train a Naive Bayes Classifier and then pull
#                     100 tweets based on a keyword to determine the sentiment 
# Revision History  : Version 1
####################################################################################


import twitter
import csv
import time
import pandas as pd
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

#compile 100 tweets based on a keyword that was entered 
def buildTestSet(search_keyword):

     #use twitters api to pull data 
     try:
          tweets_fetched = twitter_api.GetSearch(search_keyword, count = 100)

          print("I got " + str(len(tweets_fetched)) + " tweets for the word " + search_keyword)

          return[{"text":status.text, "label":None} for status in tweets_fetched]
     except Exception as e:
          print("fetch exception" + str(e))
          return None

search_term = input("Enter a search keyword: ")
testDataSet = buildTestSet(search_term)

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

#open the saved file of data and write it into a array of dictionaries 
def openFile():
     theList = []
     with open('test.csv', 'r') as csvfile:
          lineReader  = csv.reader(csvfile, delimiter =',', quotechar = "\"")
          for row in lineReader:
               #print(row)
               theList.append({"tweet_id": row[0], "text":row[1],"label":row[2], "topic":row[3]})
     return theList

trainingData = openFile()


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
          
#nltk.download('stopwords')
#nltk.download('punkt')


#trainingData = buildTrainingSet('corpus.csv', 'test2.csv')


tweetProcessor = PreProcessTweets()
preprocessedTrainingSet = tweetProcessor.processTweets(trainingData)
preprocessedTestSet = tweetProcessor.processTweets(testDataSet)

#a function that will build our word feature vector for each tweet 
def buildVocabulary(preprocessedTrainingData):
    all_words = []
    
    for (words, sentiment) in preprocessedTrainingData:
        all_words.extend(words)

    wordlist = nltk.FreqDist(all_words)
    word_features = wordlist.keys()
    
    return word_features


#assigns trues and falses for each token(word) in the tweet, for each word that is true, it exists
def extract_features(tweet):
    tweet_words=set(tweet)
    features={}
    for word in word_features:

        features['contains(%s)' % word]=(word in tweet_words)
    return features 


# Now we can extract the features and train the classifier 
word_features = buildVocabulary(preprocessedTrainingSet)
trainingFeatures=nltk.classify.apply_features(extract_features,preprocessedTrainingSet)

NBayesClassifier=nltk.NaiveBayesClassifier.train(trainingFeatures)

#if the word is true(it exists) and the vocabulary has determined it to be a bad word, assigns it a negative sentiment
NBResultLabels = [NBayesClassifier.classify(extract_features(tweet[0])) for tweet in preprocessedTestSet]

# ------------------------------------------------------------------------
# get the majority vote
if NBResultLabels.count('positive') > NBResultLabels.count('negative'):
    print("Overall Positive Sentiment")
    print("Positive Sentiment Percentage = " + str(100*NBResultLabels.count('positive')/len(NBResultLabels)) + "%")
else: 
    print("Overall Negative Sentiment")
    print("Negative Sentiment Percentage = " + str(100*NBResultLabels.count('negative')/len(NBResultLabels)) + "%")











     
