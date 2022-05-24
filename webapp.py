from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth
from flask import render_template

import pprint
import os
import pymongo

app = Flask(__name__)

app.debug = False
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app.secret_key = os.environ['SECRET_KEY']
oauth = OAuth(app)
oauth.init_app(app)

github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'],
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

connection_string = os.environ["MONGO_CONNECTION_STRING"]
db_name = os.environ["MONGO_DBNAME"]

client = pymongo.MongoClient(connection_string)
db = client[db_name]
collection = db['data']
#print(collection)


@app.context_processor
def inject_logged_in():
    return {"logged_in":('github_token' in session)}

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='http'))

@app.route('/logout')
def logout():
    session.clear()
    return render_template('message.html', message='logged out')

@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None:
        session.clear()
        message = 'Access denied: reason=' + request.args['error'] + 'error=' + request.args['error_description'] + 'full=' + pprint.pformat(request.args)
    else:
        try:
            session['github_token'] = (resp['access_token'], '')
            session['user_data']=github.get('user').data
            message='You were successfully logged in as ' + session['user_data']['login'] + '.'
        except Exception as inst:
            session.clear()
            print(inst)
            message='Unable to login, please try again.'
    return render_template('message.html', message=message)

#print(collection.find_one(comment1))

#comment1: Kendall and Kylie
@app.route('/page1', methods = ["POST", "GET"])
def renderPage1():
    #request.form["form"]
    if request.method=="GET":
        return render_template('page1.html')
    else:
<<<<<<< HEAD
        if "comment1" in request.form and len(request.form["comment1"])>0:

            thisdict = {
        #"_id":{"$oid":"6273feb0beb82ed58395294a"},
            "username":github.get('user').data,
            "post1":request.form["comment1"],
        #"post2":"comment2",
        #"post3":"comment3",
            "celebrity1":"Kendall"
        #"celebrity2":"Blake",
        #"celebrity3":"Emma"
            }
            print(collection)
            print(collection.find_one())

            collection.insert_one(thisdict)
            return render_template('page1.html')

        elif "comment2" in request.form and len(request.form["comment2"])>0:
            thisdict = {
            "username":github.get('user').data,
            #"post1":request.form["comment1"],
            "post2":request.form["comment2"],
            #"post3":"comment3",
            #"celebrity1":"Kendall",
            "celebrity2":"Blake"
            #"celebrity3":"Emma"
            }
            print(collection)
            print(collection.find_one())

            collection.insert_one(thisdict)
            return render_template('page1.html')

        elif "comment3" in request.form and len(request.form["comment3"])>0:
            thisdict={
            "username":github.get('user').data,
            #"post1":request.form["comment1"],
            #"post2":"comment2",
            "post3":request.form["comment3"],
            #"celebrity1":"Kendall",
            #"celebrity2":"Blake",
            "celebrity3":"Emma"
            }
            print(collection)
            print(collection.find_one())

            collection.insert_one(thisdict)
            return render_template('page1.html')
        else:
            return render_template('message.html', message='Error: An empty comment was submitted. Please type something in and try again!')
"""
#comment2: Blake
@app.route('/page1', methods = ["POST", "GET"])
def renderPage1():
    if request.method=="GET":
        return render_template('page1.html')
    else:
    #request.form["form"]
        if "comment2" in request.form:
            thisdict = {
            "username":github.get('user').data,
            #"post1":request.form["comment1"],
            "post2":request.form["comment2"],
            #"post3":"comment3",
            #"celebrity1":"Kendall",
            "celebrity2":"Blake",
            #"celebrity3":"Emma"
            }

            print(collection)
            print(collection.find_one())

            collection.insert_one(thisdict)
            return render_template('page1.html')
        else:
            return render_template('message.html', message='Error: An empty comment was submitted. Please type something in and try again!')

#comment3: Emma
@app.route('/page1', methods = ["POST", "GET"])
def renderPage1():
    if request.method=="GET":
        return render_template('page1.html')
    else:
        if "comment3" in request.form:
            thisdict={
            "username":github.get('user').data,
            #"post1":request.form["comment1"],
            #"post2":"comment2",
            "post3":request.form["comment3"],
            #"celebrity1":"Kendall",
            #"celebrity2":"Blake",
            "celebrity3":"Emma"
            }
            print(collection)
            print(collection.find_one())

            collection.insert_one(thisdict)
            return render_template('page1.html')
        else:
            return render_template('message.html', message='Error: An empty comment was submitted. Please type something in and try again!')

"""
=======
        print(inst)
        message=""
        return render_template('page1.html')
 


>>>>>>> e5e5349750b9327cfe697b10cefaeaf61d5f64aa
@github.tokengetter
def get_github_oauth_token():
    return session['github_token']


if __name__ == '__main__':
    app.run(debug=True)
