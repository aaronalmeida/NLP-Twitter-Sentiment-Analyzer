# Twitter-Sentiment-Analyzer
Determines the sentiment of a topic based on a collection of recent tweets 


Again the obligatory meme!

![alt text](https://github.com/aaronalmeida/Twitter-Sentiment-Analyzer/blob/master/meme.jpg)


## Technologies used
- Python 3
- Natural Language Toolkit

## Data Source
- Twitter corpus
- [Twitter's API](https://developer.twitter.com/)

## Features
- Includes already pulled tweets from the database 
- Keyword Search

## Collector 
The collector will use the corpus file containing the tweet_ids and pull each tweet individually. This process takes about 10 hours as Twitters API has a limit of 180 requests every hour for a standard API key. The data is saved in another .csv file. 

## Processor 
The purpose of the preprocessor is clean up the tokens (words) to ensure the classifier reads the word for what it's supposed to be 
- Replaces all the @ mentions
- Removes URL's (pictures, tweet link, etc.)
- Hashtags (probably important, would be implemented in the future) 
- Repeated characters that would otherwise not be used for actual spelling (helloooooooooooo to hello)

## Classifier 

- The data will be processed using the Naive Bayes Classifier 
- The algorithm uses the corpus data with positive and negative labels to train the classifier 
- The vocabulary is built using the corpus data, labeling the words as positive, negative or neutral 
- The tweets are then compared to all the words in the vocabulary, marking their existence as true or false 
- Determines if the tweet is positive or negative based on how many words in the tweet are positive or negative 


## Future Implementation 
- Find the trending topics & automatically determine its sentiment 
- Find sentiment of a keyword at a certain point in time 
- Implement sentiment during a stock analysis
