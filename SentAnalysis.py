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
import re
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords 



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





######################################
search_term = input("Enter a search keyword: ")
testDataSet = buildTestSet(search_term)

trainingData = openFile()
tweetProcessor = PreProcessTweets()
preprocessedTrainingSet = tweetProcessor.processTweets(trainingData)
preprocessedTestSet = tweetProcessor.processTweets(testDataSet)

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






     
