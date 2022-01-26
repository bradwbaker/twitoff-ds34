from flask_sqlalchemy import SQLAlchemy


# create a db object
DB = SQLAlchemy()

# create a table with a specific schema
# we will do that by creating a python class.

class User(DB.Model):
    # two columns inside of our user table
    # ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # username column schema
    username = DB.Column(DB.String, nullable=False)


class Tweet(DB.Model):
    # ID column schema
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    # text column schema
    text = DB.Column(DB.Unicode(300), nullable=False)
    # user column schema (secondary/ foreign key)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    # set up a relationship between the tweets and the uses
    # will automatically create the one-to-many relationship, but also add a new attribute
    # onto the "User" called "Tweets" which will be a list of all of the user tweets
    user = DB.relationship("User", backref=DB.backref('tweets'), lazy=True)