from shop import db,login_manager
from datetime import datetime
from flask_login import UserMixin
import json

'''
This takes the id as input sets the callback for reloading a user from the session.
User_loader (user defined function) is decorated by user_loader of flask
'''
@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

'''
To make implementing a user class easier, we are inheriting from UserMixin, 
which provides default implementations for properties and methods like is_authenticated etc. 
'''
class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    #f_name = db.Column(db.String(50), unique= False)
    username = db.Column(db.String(50), unique= True)
    email = db.Column(db.String(50), unique= True)
    password = db.Column(db.String(200), unique= False)
    #country = db.Column(db.String(50), unique= False)
    state = db.Column(db.String(50), unique= False)
    city = db.Column(db.String(50), unique= False)
    contact = db.Column(db.String(50), unique= False)
    address = db.Column(db.String(50), unique= False)
    pincode = db.Column(db.String(50), unique= False)
    profile = db.Column(db.String(200), unique= False , default='profile.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Register %r>' % self.name

'''Allows the creation of types which add additional functionality to an existing type.'''
class JsonEncodedDict(db.TypeDecorator):
    #Text - A variably sized string type.
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            #JSON.dumps-python to json
            return json.dumps(value)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            #JSON value to python
            return json.loads(value)

#creating customer order table
class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEncodedDict)
    

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice


db.create_all()
