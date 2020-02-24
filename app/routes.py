import os
from app import app
from flask import render_template, request, redirect, session, url_for
from flask_pymongo import PyMongo

app.config['MONGO_DBNAME'] = 'IA'

app.secret_key = b'\x1a\xaf3\x7f\x8b>\x80\xbe\xd4%C\x8e\xd9\xf70\xfan\xd4i\x1a!\x17\xf9\x1d'

app.config['MONGO_URI'] = 'mongodb+srv://admin:yEXc16X4d8OuM8b0@cluster0-3ainf.mongodb.net/IA?retryWrites=true&w=majority'

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')

def index():
    user_info = dict(request.form)
    print(user_info)
    return render_template('index.html')


@app.route('/add', methods = ["get", "post"])
def add():
    user_info = dict(request.form)
    event_name = user_info["name"]
    event_date = user_info["date"]
    event_category = user_info["category"]
    event_time = user_info["description"]
    collection = mongo.db.events
    collection.insert({"name": event_name, "date": event_date, "category": event_category, "time": event_time})
    return redirect('/homepage')
@app.route('/signup1', methods = ["get", "post"])
def signup():
    user_info = dict(request.form)
    print(user_info)
    email = user_info["email"]
    password = user_info["password"]
    name = user_info["name"]
    collection = mongo.db.information
    query = list(collection.find({"email": email}))
    if len(query) > 0:
        return render_template('error.html', error = "Account was already created!", link = "/signup")
    elif len(query) == 0:
        if email.endswith('@dwight.edu'):
            collection.insert({"email": email, "password": password, "name": name})
            return render_template('error.html', error = "Account was succesfully created!", link = "/signup")
        else:
            return render_template('error.html', error = "Email is not apart of dwight.", link = "/signup")

@app.route('/signup')
def test():
    return render_template('signup.html')

@app.route('/login', methods = ["get", "post"])
def login():
    user_info = dict(request.form)
    print(user_info)
    email = user_info["email"]
    password = user_info["password"]
    collection = mongo.db.information
    query = list(collection.find({"email": email}))
    print(query)
    if len(query) > 0:
        if query[0]["password"] == password:
            session['username'] = email
            return redirect('/homepage')
        else:
            return "error"
    else:
        return render_template('error.html', error = "Account does not exist", link = "/index")
@app.route('/homepage')
def homepage():
    collection = mongo.db.events
    events = collection.find({})
    return render_template('homepage.html', events = events)
@app.route('/filter', methods = ["get", "post"])
def function():
    collection = mongo.db.events
    user_input = dict(request.form)
    category = user_input["category"]
    test = list(collection.find({"category": category}))
    return render_template('filteredevents.html', events = test)
@app.route('/addevent')
def display():
    return render_template('addevent.html')
