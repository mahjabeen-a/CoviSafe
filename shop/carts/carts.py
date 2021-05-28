from flask import request, session, url_for, redirect, render_template, flash, current_app
from shop import app, db
from shop.products.models import Product
from shop.products.routes import brands, categories

def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1  + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart', methods=['POST'])
def Addcart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        product = Product.query.filter_by(id=product_id).first()

        if request.method =="POST":
            DictItems = {product_id:{'name':product.name,'price':float(product.price),'discount':product.discount,'color':color,'quantity':quantity,'image':product.image_1, 'colors':product.colors}}
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    # increasing the count of already added product
                    for key, val in session['Shoppingcart'].items():
                        if int(key) == int(product_id):
                            session.modified = True
                            val['quantity'] = int(val['quantity']) + 1
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                # Shoppingcart is a key in session (which is a dictionary)
                # session is for the given cart
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    #updatecart and deleteitem and navbar.html calls this
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax =("%.2f" %(.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('products/carts.html',tax=tax, grandtotal=grandtotal, brands=brands(), categories=categories())

@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method =="POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item is updated!')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:id>')
def deleteitem(id):
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key , item in session['Shoppingcart'].items():
            if int(key) == id:
                #if key not present, return none
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearcart():
    try:
        #to pop out this particular session
        session.pop('Shoppingcart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
    