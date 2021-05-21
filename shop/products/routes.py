from flask import request,url_for,redirect,render_template,flash
from shop import app,db
from .models import Brand,Category

#adding the brand to the database
@app.route('/addbrand',methods=['GET','POST'])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database','success')
        return redirect(url_for('addbrand'))
        db.session.commit()
    return render_template('products/addbrand.html',brands='brands')

#adding the category to the database
@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if request.method == "POST":
        getbrand = request.form.get('category')
        cat = Brand(name=getbrand)
        db.session.add(cat)
        flash(f'The category {getbrand} was added to your database','success')
        return redirect(url_for('addcat'))
        db.session.commit()
    return render_template('products/addbrand.html')