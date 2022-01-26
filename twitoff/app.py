from flask import Flask, render_template
from .models import DB, User, Tweet

def create_app():

    app = Flask(__name__)
    
    # configuration variable to our app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
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

        #remove everything from the DB
        DB.drop_all()
        # recreate the User and Tweet tables
        # so that they're ready to be used (inserted into)
        DB.create_all()
        

        # make two new users
        ryan = User(id=1, username='ryanallred')
        bradley = User(id=2, username='bradbaker')

        # make two tweets
        tweet1 = Tweet(id=1, text="this is ryan's tweet", user=ryan)
        tweet2 = Tweet(id=3, text="hey my name is ryan", user=ryan)
        tweet3 = Tweet(id=4, text="I teach data science", user=ryan)
        tweet4 = Tweet(id=2, text="this is bradley's tweet", user=bradley)
        tweet5 = Tweet(id=5, text="My name is Bradley", user=bradley)
        tweet6 = Tweet(id=6, text="I am a student", user=bradley)

        # inserting into the DB when working with SQLite directly
        DB.session.add(ryan)
        DB.session.add(bradley)
        DB.session.add(tweet1)
        DB.session.add(tweet2)
        DB.session.add(tweet3)
        DB.session.add(tweet4)
        DB.session.add(tweet5)
        DB.session.add(tweet6)

        # commit the DB changes
        DB.session.commit()

        return render_template('base.html', title='Populate')
        # make two tweets and attach the tweets to those users

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