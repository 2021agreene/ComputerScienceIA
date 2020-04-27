import os
from app import app
from flask import render_template, request, redirect, session, url_for
from flask_pymongo import PyMongo
from flask import Flask
from bson.objectid import ObjectId
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

#s = URLSafeTimedSerializer('Thisisasecret')
#app.config.from_pyfile('config.cfg')
#mail = Mail(app)
app.config['MONGO_DBNAME'] = 'IA'

if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = b'\x1a\xaf3\x7f\x8b>\x80\xbe\xd4%C\x8e\xd9\xf70\xfan\xd4i\x1a!\x17\xf9\x1d'

app.config['MONGO_URI'] = 'mongodb+srv://admin:yEXc16X4d8OuM8b0@cluster0-3ainf.mongodb.net/IA?retryWrites=true&w=majority'

mongo = PyMongo(app)

login = True
@app.route('/')
@app.route('/index')
def index():
    user_info = dict(request.form)
    return render_template('index.html')
@app.route('/add', methods = ["get", "post"])
def add():
    user_info = dict(request.form)
    event_name = user_info["name"]
    event_date = user_info["date"]
    event_category = user_info["category"]
    event_description = user_info["description"]
    collection = mongo.db.events
    collection.insert({"name": event_name, "date": event_date, "category": event_category, "description": event_description})
    return redirect('/homepage')
@app.route('/signup1', methods = ["get", "post"])
def signup():
    user_info = dict(request.form)
    email = user_info["email"]
    password = user_info["password"]
    name = user_info["name"]
    collection = mongo.db.information
    query = list(collection.find({"email": email}))
    #token = s.dumps(email, salt ='email-confirm')
    #msg = Message('Confirm Email', sender='dwightcaswebsite@gmail.com', recipients = [email])
    #link = url_for('confirm_email', token = token, _external=True)
    #msg.body = 'Your link is {}'.format(link)
    #mail.send(msg)
    #print(token)
    if len(query) > 0:
        return render_template('error.html', error = "Account was already created!", link = "/signup")
    elif len(query) == 0:
        if email.endswith('@dwight.edu'):
            collection.insert({"email": email, "password": password, "name": name})
            return render_template('error.html', error = "Account was succesfully created!", link = "/signup")
        else:
            return render_template('error.html', error = "Email is not apart of dwight.", link = "/signup")
@app.route('/confirmemail/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=20)
    except SignatureExpired:
        return "the token is expired"
    return "the token works"
@app.route('/signup')
def test():
    return render_template('signup.html')
@app.route('/login', methods = ["get", "post"])
def login():
    global login
    user_info = dict(request.form)
    email = user_info["email"]
    password = user_info["password"]
    collection = mongo.db.information
    query = list(collection.find({"email": email}))
    if len(query) > 0:
        if query[0]["password"] == password:
            session['username'] = email
            login = True
            return redirect('/homepage')
        else:
            return "error"
    else:
        return render_template('error.html', error = "Account does not exist", link = "/index")
@app.route('/homepage')
def homepage():
    global login
    test = "none"
    if login == True:
        collection = mongo.db.events
        events = list(collection.find({}))
        if len(events) > 0:
            test = "all"
        return render_template('homepage.html', events = events, test = test)
    else:
        return redirect('/index')
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
@app.route('/delete', methods = ["get", "post"])
def delete():
    collection = mongo.db.events
    user_input = dict(request.form)
    delete = user_input["_id"]
    collection.delete_one({"_id": ObjectId(delete)})
    return redirect('/homepage')
@app.route('/details', methods = ["get", "post"])
def details():
    collection = mongo.db.events
    user_input = dict(request.form)
    name = user_input["_id"]
    list = collection.find({"_id": ObjectId(name)})
    return render_template('details.html', events = list)
@app.route('/register', methods = ["get", "post"])
def register():
    return render_template('register.html')
@app.route('/registeradd', methods = ["get", "post"])
def registeradd():
    user_input = dict(request.form)
    collection = mongo.db.attendies
    event_name = user_input["ename"]
    your_name = user_input["uname"]
    event_email = user_input["email"]
    list = collection.insert({"name": event_name, "yourname": your_name, "email": event_email})
    return redirect('/homepage')
@app.route('/attending')
def attending():
    return render_template('viewform.html')
@app.route('/viewattendies', methods = ["get", "post"])
def attendies():
    user_input = dict(request.form)
    collection = mongo.db.attendies
    event_name = user_input["name"]
    list = collection.find({"name": event_name})
    return render_template('viewattendies.html', events = list)
