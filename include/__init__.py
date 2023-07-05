from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "0b2c495c7a1b941de0d8422927a9d93a"
app.config["MONGO_URI"] = "mongodb+srv://rishithakkar48:Sh0JndMyKmzYqbaF@cluster0.vmwh2oz.mongodb.net/todo-list"

bcrypt = Bcrypt(app)    # setup bcrypt for password hashing

# setup mongodb
mongo = PyMongo(app)
db_con = mongo.db

from include import routes
