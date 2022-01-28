"""This is what brings the application together"""
from os import getenv
from flask import Flask, render_template, request
from .predict import predict_user
from .models import DB, User, Tweet
from .twitter import add_or_update_user


def create_app():
    """
    The main app function for twitoff.
    Brings everything together.
    """
    # __name__ is the name of the current path module
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title="Home", users=User.query.all())

    @app.route('/update')
    def update():
        '''update all users'''
        usernames = get_usernames()
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html', title='All users have been updated.')

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Database has been reset.")

    @app.route('/user', methods=["POST"])
    @app.route('/user/<username>', methods=["GET"])
    def user(username=None, message=''):
        # we either take name that was passed in or we pull it
        # from our request.values which would be accessed through the
        # user submission
        username = username or request.values['user_name']
        try:
            if request.method=='POST':
                add_or_update_user(username)
                message = f"User {username} has been succesfully added!"
            tweets = User.query.filter(User.username == username).one().tweets
        except Exception as e:
            message = f"Error adding {username}: {e}"
            tweets = []

        return render_template("user.html", title=username, tweets=tweets, message=message)

    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values["user1"]])

        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            # prediction returns a 0 or 1
            prediction = predict_user(
                user0, user1, request.values["tweet_text"])
            message = "'{}' is more likely to be said by {} than {}!".format(
                request.values["tweet_text"],
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title="Prediction", message=message)

    return app


def get_usernames():
    # get all usernames of existing users
    Users = User.query.all()
    usernames= []
    for user in Users:
        usernames.append(user.username)

    return usernames