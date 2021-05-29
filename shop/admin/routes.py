from json.decoder import JSONDecodeError
from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import Admin
from shop.products.models import Product, Brand, Category
from shop.customers.models import CustomerOrder, Customer, JsonEncodedDict
import os

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Please login first','danger')
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('admin/index.html', title='Admin Page',products=products)

@app.route('/brands')
def brands():
    if 'email' not in session:
        flash('Please login first','danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='brands',brands=brands)

@app.route('/category')
def category():
    if 'email' not in session:
        flash('Please login first','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='categories',categories=categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = Admin(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password)
        #add and commit the current user's entry
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} ! Thanks for registering', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Registration Page")


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data} ! You are loggedin now','success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong email or password', 'danger')
    return render_template('admin/login.html',title='Login page',form=form)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

#view customer orders
@app.route('/orders')
def orders_recieved():
    if 'email' not in session:
        flash('Please login first','danger')
        return redirect(url_for('login'))
    #orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
    #cust_orders = CustomerOrder.query.join(Customer, (CustomerOrder.customer_id == Customer.id)).add_columns(CustomerOrder.id, CustomerOrder.invoice, CustomerOrder.customer_id, Customer.address, Customer.city, Customer.state, Customer.pincode).all()
    cust_orders = db.session.query(CustomerOrder, Customer).filter(CustomerOrder.customer_id == Customer.id).order_by(CustomerOrder.date_created.desc()).all()
    return render_template('products/orders.html', title='Orders',cust_orders=cust_orders)
