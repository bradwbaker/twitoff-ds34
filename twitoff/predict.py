from .models import User
from sklearn.linear_model import LogisticRegression
import numpy as np
from .twitter import vectorize_tweet

def predict_user(user0_username, user1_username, hypo_tweet_text):
    '''
    Determine and returns which user is more likely to say a given tweet
    Example run: predict_user("elonmusk", "jackblack", "Tesla cars go vroom")
    Returns a 0 (user0_name: "elonmusk") or a 1 (user1_name: "jackblack")
    '''

    # Query for the two users so that we can get their word embeddings
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # get the word embeddings of the tweets of both users 0 and 1. 
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # combine the two users word embeddings into on e big *2D* NumPy array
    # this is essentially our X matrix for training our logistic regression
    vects = np.vstack([user0_vects, user1_vects])


    # create a np array to represent the y vector 
    # was the author of any given word embedding

    labels = np.concatenate([np.zeros(len(user0.tweets)),
                             np.ones(len(user1.tweets))])


    # import and train our logisitic regression
    log_reg = LogisticRegression()

    # train our logistic regression
    log_reg.fit(vects, labels)

    # get the word embeddigs for our hypo_tweet_text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # generate a prediction
    prediction = log_reg.predict([hypo_tweet_vect])

    return prediction[0]
