from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
from flask_msearch import Search
from flask_login import LoginManager, login_manager

#getting the path of shop
basedir = os.path.abspath(os.path.dirname(__file__))

#passing the current module as a parameter, returns object
app = Flask(__name__)
#URI - Uniform Resource Identifier
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covisafe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'spooprathmahj142815'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')

#for photo upload
photos = UploadSet('photos', IMAGES)    #IMAGES-extensions(jpg,jpeg,etc)
configure_uploads(app, photos)      #links the UploadSet with the flask object app
patch_request_class(app)        #max upload size(16 megabytes)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customerLogin'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u'Please login first'


from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes