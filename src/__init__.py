from flask import Flask
import os

from flask.cli import with_appcontext
from sqlalchemy import event

from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# for password hashing
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)
CORS(app)
# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# load the secret key defined in the .env file
app.secret_key = os.environ.get("SECRET_KEY")
bcrypt = Bcrypt(app)

# Path for our local sql lite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")

# To specify to track modifications of objects and emit signals
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")


# sql alchemy instance
db = SQLAlchemy(app)


# Flask Migrate instance to handle migrations
migrate = Migrate(app, db)

# import api blueprint to register it with app
from src.routes import api
app.register_blueprint(api, url_prefix="/api")

# import models to let the migrate tool know
from src.models.user_model import User
from src.models.store_models import Store
from src.models.category_model import Category
from src.models.requests import ApprovalRequests
from src.models.product_model import Product
from src.models.cart import cart


@app.cli.command('add_initial_data')
@with_appcontext
def add_entry_to_db(*args, **kwargs):
    if User.query.first() is None:
        new_entry = User(
            userid="admin1",
            usertype =2,
            name= "admin1 ",
            email= "admin1@gmail.com",
            password= bcrypt.generate_password_hash('admin1').decode('utf-8')
        )
        db.session.add(new_entry)
        db.session.commit()
        print('Entry added to the database')