# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 14:27:31 2020

@author: prabhakar reddy
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 14:06:56 2020

@author: prabhakar reddy



"""
import GetOldTweets3 as got
import pandas as pd
import regex as re
import datetime as dt
import sqlite3


username = 'PpollingNumbers'
count = 200
# Creation of query object
tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                        .setMaxTweets(count)
# Creation of list that contains all tweets
tweets = got.manager.TweetManager.getTweets(tweetCriteria)
# Creating list of chosen tweet data
user_tweets = [[tweet.date, tweet.text] for tweet in tweets]
tweet_date = [[tweet.date] for tweet in tweets]
date_df= pd.DataFrame(tweet_date, columns=['date'])
#date_df['date'] = date_df['date'].dt.date
#print(user_tweets)

# count = 0
# for i in range(0,len(date_df)):
#     if date_df['date'][i] == dt.date.today():
#         count = count+1
 # local time                   

def val_append(user_tweets):
        
    test_words = ['National Poll','Trump','Biden']
    contains_all = True
    trump = []
    biden = []
    date = []
    tweet = []   
    
    for tweets in user_tweets:
        if all(x in str(tweets) for x in test_words):
            print('yes')
        
            date.append(tweets[0])  
            tweet.append(tweets[1])           
            b = str(tweets).split(' ')
            
            for i in range(0, len(b)):
                if b[i] =='Trump':
                    temp = b[i+1][:2]
                    if temp.isdigit() ==True:
                        trump.append(temp)
                    
                elif b[i]=='Biden':
                    temp = b[i+1][:2]
                    if temp.isdigit() ==True:
                        biden.append(temp)
    return date, trump, biden



       

Final_df = pd.DataFrame(list(zip(date,trump, biden)), columns=['Date', 'Trump', 'Biden' ])        
       

    