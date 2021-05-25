from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators
from flask_wtf.file import FileRequired, FileAllowed, FileField

class CustomerRegistrationForm(Form):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()]) #needs email validator to be installed -> wtforms[email]
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    country = StringField('Country: ', [validators.DataRequired()])
    state = StringField('State: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = StringField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()])
    pincode = StringField('Pin Code: ', [validators.DataRequired()])

    profile = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Only image allowed!')])

    submit = SubmitField('Register')
    
