import action
import os
from flask import Flask, request, render_template, redirect, session, Session, send_file
from flask_pymongo import PyMongo

app = Flask(__name__)

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super_secret_key'
session = Session()
app.config["MONGO_URI"] = "mongodb://localhost:27017/KbDPES"

mongo = PyMongo(app)


@app.route('/', methods = ["GET", "POST"])
def hello_world():
    if 'username' in session:
        return redirect('/details')
    else:
        return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    users = mongo.db.users
    existing_user = users.find_one({'username': username})

    if existing_user is None:
        session['temp_username'] = username
        session['temp_password'] = password
        return render_template('register.html', username=username, password=password)
    else:
        if password == existing_user['password']:
            session['username'] = username
            return redirect('/details')
        else:
            return redirect('/error')


@app.route('/registered', methods=["POST"])
def registered():
    users = mongo.db.users
    username = session['temp_username']
    password = session['temp_password']
    first_name = request.form['fname']
    last_name = request.form['lname']
    age = request.form['age']
    gender = request.form['gender']
    users.insert({'username': username, 'password': password, 'fname': first_name, 'lname': last_name,
              'age': age, 'gender': gender})
    session.pop('temp_username', None)
    session.pop('temp_password', None)
    session['username'] = username
    return redirect('/details')


@app.route('/details')
def details():
    session_username = session['username']
    user = mongo.db.users
    username = user.find_one({'username': session_username})
    first_name = username['fname']
    last_name = username['lname']
    name = first_name + " " + last_name
    gender = username['gender']
    age = username['age']
    return render_template('details.html', username=session_username, name=name, gender=gender, age=age)


@app.route('/predict')
def predict():
    return render_template('status.html', result='The symptoms point to a 90% chance of Common Cold.')


@app.route('/error')
def error():
    return render_template('index.html', error_message="Please check the credentials")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/delete_<username>')
def delete_user(username):
    user = mongo.db.users
    username = user.find_one({'username': username})
    user.remove(username)
    return 'Removed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
