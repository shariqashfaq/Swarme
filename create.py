import os

from flask import Flask

#import table definitions
from models import *

app = Flask(__name__)


#tell Flask what sqlalchemy database to use
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#prepare application to work with sqlalchemy
db.init_app(app)

def main():
    #create tables based on each table definition in models
    db.create_all()

if __name__=="__main__":
    #allows for command line interaction with flask application
    with app.app_context():
        main()