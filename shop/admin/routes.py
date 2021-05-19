from flask import render_template,session, request, redirect, url_for
from shop import app, db

@app.route('/')
def home():
    return "Home page of your shop"

@app.route('/register')
def register():
    return render_template('admin/register.html',title='Register user')