from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
#URI - Uniform Resource Identifier
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covisafe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'spooprathmahj142815'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from shop.admin import routes