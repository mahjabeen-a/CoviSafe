from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#URI - Uniform Resource Identifier
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covisafe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from shop import routes