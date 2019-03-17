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



'''
@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name': 'Vyom'})
    return 'Added User!'
'''


@app.route('/capture', methods=["GET", "POST"])
def capture():
    return send_file(app.root_path + "/capture.py")


@app.route('/registered', methods=["POST"])
def registered():
    users = mongo.db.users
    username = session['temp_username']
    password = session['temp_password']
    ip_address = request.form['ip']
    ssh_username = request.form['ssh_username']
    ssh_password = request.form['ssh_password']
    try:
        s = 'sshpass -p "'+ssh_password+'" ssh-copy-id -o StrictHostKeyChecking=no '+ssh_username+'@'+ip_address
        os.system(s)
    except:
        return render_template('register.html', username=username, password=password, error_message='Please check the ssh details')
    else:
        users.insert({'username': username, 'password': password, 'ip': ip_address, 'ssh_username': ssh_username,
                  'ssh_password': ssh_password})
        session.pop('temp_username', None)
        session.pop('temp_password', None)
        session['username'] = username
        return redirect('/details')


@app.route('/details')
def verify():
    return render_template('details.html')


@app.route('/error')
def error():
    return render_template('index.html', error_message="Please check the credentials")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


'''
@app.route('/update')
def update():
    user = mongo.db.users
    crimson = user.find_one({'name' : 'crimson_carnival'})
    crimson['password'] = 'Hello World'
    user.save(crimson)
    return 'Updated crimson_carnival'
'''


@app.route('/delete_<username>')
def delete_all(username):
    user = mongo.db.users
    vyom = user.find_one({'username': username})
    user.remove(vyom)
    return 'Removed'


@app.route('/remove__<name>')
def delete_employee(name):
    user = mongo.db.employees
    vyom = user.find_one({'name': name})
    user.remove(vyom)
    return 'Removed'


@app.route('/store', methods=["POST"])
def test():
    ip_address = request.form['ip']
    ssh_username = request.form['ssh_username']
    ssh_password = request.form['ssh_password']
    if ssh_password != '':
        try:
            s = 'sshpass -p "'+ssh_password+'" ssh-copy-id -o StrictHostKeyChecking=no '+ssh_username+'@'+ip_address
            os.system(s)
        except:
            return render_template("details.html", error_message='Please check the ssh details')
        else:
            user = mongo.db.users
            single_user = user.find_one({'username': session['username']})
            single_user['ssh_password'] = ssh_password
            single_user['ssh_username'] = ssh_username
            single_user['ip'] = ip_address
            user.save(single_user)
    path = request.form['path']
    result = action.do(path, session['username'])
    return render_template("status.html", result=result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
