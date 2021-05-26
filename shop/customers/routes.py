#routes for customers

from shop.products.models import Addproduct
from shop.admin.routes import category
from flask import request, session, url_for, redirect, render_template, flash, current_app, make_response
from flask_login import login_required,current_user,login_user,logout_user
from shop import app, db, photos, search, bcrypt,login_manager
from .forms import CustomerRegistrationForm,CustomerLoginForm
from .models import Register,CustomerOrder
from shop.products.routes import brands, categories
import secrets, os
import pdfkit
import stripe

#enter the keys as given in your stripe webpage
publishable_key = 'pk_test_51IvDSkSF76dLNO0kL60OspwKhL5Kk2f3aCKhEJqNOb11qBAgxY2b1njLus2zap4WIV4Qqg0aQCYEWqQsTlqTIvqj00ddCtdsVo'
stripe.api_key = ''

@app.route('/payment',methods=['POST'])
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
      email=request.form['stripeEmail'],
      source=request.form['stripeToken'],
    )
    charge = stripe.Charge.create(
      customer=customer.id,
      description='Myshop',
      amount=amount,
      currency='inr',
    )
    orders =  CustomerOrder.query.filter_by(customer_id = current_user.id,invoice=invoice).order_by(CustomerOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
    return render_template('customer/thank.html')

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
            #login
            login_user(user)
            flash('You are logged in now!','success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        else:
            flash('Incorrect email or password','danger')
            return redirect (url_for('customerLogin'))
    return render_template('customer/login.html' ,form=form)

#default get method
@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

#remove unwanted attributes from the session
def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
        del shopping['colors']
    return updateshoppingcart
        
@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        updateshoppingcart
        try:
            #orders is of type JsonEncodedDict
            for key, val in session['Shoppingcart'].items():
                updateprod = Addproduct.query.get_or_404(int(key))
                updateprod.stock -= int(val['quantity'])
                db.session.commit()

            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully!', 'success')
            return redirect(url_for('orders',invoice=invoice))
        except Exception as e:
            print(e)
            flash('Something went wrong while getting order!','danger')
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grandtotal = 0
        subtotal = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for key, product in orders.orders.items():
            discount = (product['discount']/100) * float(product['price'])
            subtotal += float(product['price']) * int(product['quantity'])
            subtotal -= discount
            tax = ("%.2f" % (.06 * float(subtotal)))
            grandtotal = ("%.2f" % (1.06 * float(subtotal)))
    else:
        return redirect(url_for('customerLogin'))
    return render_template('customer/order.html', invoice=invoice, tax=tax, subtotal=subtotal, grandtotal=grandtotal, customer=customer, orders=orders, brands=brands(), categories=categories())

@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grandtotal = 0
        subtotal = 0
        customer_id = current_user.id
        if request.method == 'POST':
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for key, product in orders.orders.items():
                discount = (product['discount']/100) * float(product['price'])
                subtotal += float(product['price']) * int(product['quantity'])
                subtotal -= discount
                tax = ("%.2f" % (.06 * float(subtotal)))
                grandtotal = ("%.2f" % (1.06 * float(subtotal)))

            #configuration for pdfkit
            config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
            rendered =  render_template('customer/pdf.html', invoice=invoice, tax=tax,grandTotal=grandtotal,customer=customer,orders=orders)
            pdf = pdfkit.from_string(rendered, False, configuration=config)
            
            response = make_response(pdf)
            response.headers['content-Type'] ='application/pdf'
            response.headers['content-Disposition'] ='inline; filename='+invoice+'.pdf'
            return response
    return request(url_for('orders'))

