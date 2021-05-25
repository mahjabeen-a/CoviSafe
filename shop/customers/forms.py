from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from flask_wtf.file import FileRequired, FileAllowed, FileField
from flask_wtf import FlaskForm
from .models import Register

class CustomerRegistrationForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()]) #needs email validator to be installed -> wtforms[email]
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    #country = StringField('Country: ', [validators.DataRequired()])
    state = StringField('State: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    pincode = StringField('Pin Code: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Only image allowed!')])

    submit = SubmitField('Register')

    def validate_username(self, username):
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")
        
    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")
    
class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ',[validators.Email(), validators.DataRequired()]) #needs email validator to be installed -> wtforms[email]
    password = PasswordField('Password: ',[validators.DataRequired()])