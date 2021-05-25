#routes for customers

from shop.admin.routes import category
from flask import request, session, url_for, redirect, render_template, flash, current_app
from shop import app, db, photos, search, bcrypt
from .forms import CustomerRegistrationForm
from .models import Register
import secrets, os

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegistrationForm(request.form)
    if request.method == 'POST':
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password,state=form.state.data, city=form.city.data,contact=form.contact.data, address=form.address.data, pincode=form.pincode.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering!', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customer/register.html', form=form)