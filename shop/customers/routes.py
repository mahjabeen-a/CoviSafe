#routes for customers

from shop.admin.routes import category
from flask import request, session, url_for, redirect, render_template, flash, current_app
from flask_login import login_required,current_user,login_user,logout_user
from shop import app, db, photos, search, bcrypt,login_manager
from .forms import CustomerRegistrationForm,CustomerLoginForm
from .models import Register
import secrets, os

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,state=form.state.data, city=form.city.data,contact=form.contact.data, address=form.address.data, pincode=form.pincode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering!', 'success')
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form)


@app.route('/customer/login', methods=['GET', 'POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You are login now!','success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email and password','danger')
        return redirect (url_for('customerLogin'))
    return render_template('customer/login.html' ,form=form)
