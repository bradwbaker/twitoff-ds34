from flask import Flask, render_template
from .models import DB, User, Tweet
from os import getenv
from .twitter import add_or_update_user

def create_app():

    app = Flask(__name__)
    
    # configuration variable to our app
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # connect our database to the app object
    DB.init_app(app)

    @app.route("/")
    def home_page():
        users = User.query.all()
        print(users)
        return render_template('base.html', title='Home', users=users)
    
    @app.route('/populate')
    # test my database funtionality
    #by inserting some fake data into the DB
    def populate():
        
        add_or_update_user('nasa')
        add_or_update_user('euphoriaHBO')
        add_or_update_user('RyanAllred')

        return render_template('base.html', title='Populate')

    @app.route('/update')
    # test my database funtionality
    #by inserting some fake data into the DB
    def update():
        
        usernames = get_usernames()
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Update User Tweets')

    @app.route('/reset')
    def reset():
        # do some database stuff
        # drop old DB tables
        # remake new db tables
        #remove everything from the DB
        DB.drop_all()
        # recreate the User and Tweet tables
        # so that they're ready to be used (inserted into)
        DB.create_all()
        return render_template('base.html', title='Reset Database')

    return app


def get_usernames():
    # get all of the usernames of existing users
    Users = User.query.all()
    usernames = []
    for user in Users:
        usernames.append(user.username)
        
    return usernames