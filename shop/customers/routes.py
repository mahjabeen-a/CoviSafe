#routes for customers

from shop.admin.routes import category
from flask import request, session, url_for, redirect, render_template, flash, current_app
from shop import app, db, photos, products,search
from .forms import CustomerRegistrationForm
import secrets, os

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegistrationForm(request.form)
    return render_template('customer/register.html', form=form)