from flask import Flask, redirect, url_for, session, request, jsonify, Markup
from flask_oauthlib.client import OAuth
from flask import render_template

import pprint
import os
import pymongo

app = Flask(__name__)

#github OAUTH
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

@app.context_processor
def inject_logged_in():
    return {"logged_in":('github_token' in session)}


@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True, _scheme='http'))

@app.route('/')
def home():
    return render_template('home.html')

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

#COMMENTS
#if method = get (BEFORE posting)
@app.route('/page1', methods = ["POST", "GET"])
def renderPage1():
    if request.method == "GET":
        v1 = collection.find({"celebrity1":"Kendall"})
        v2 = collection.find({"celebrity2":"Blake"})
        v3 = collection.find({"celebrity3":"Emma"})
        formatted_posts1 = ""
        formatted_posts2 = ""
        formatted_posts3 = ""

        for post in v1:
            formatted_posts1 = formatted_posts1 + post["username"] + Markup(": ")+ post["post1"] + Markup("<br>")
        for post in v2:
            formatted_posts2 = formatted_posts2 + post["username"] + Markup(": ")+ post["post2"] + Markup("<br>")
        for post in v3:
            formatted_posts3 = formatted_posts3 + post["username"] + Markup(": ")+ post["post3"] + Markup("<br>")

        return render_template('page1.html', c1 = formatted_posts1, c2 = formatted_posts2, c3 = formatted_posts3)
#if method = post (AFTER posting)
    #comment1/Kendall
    if request.method == "POST":
        if len(request.form["comment1"])>0 or len(request.form["comment2"])>0 or len(request.form["comment3"])>0:
    #and len(request.form["comment1"])>0:
            thisdict = {
            "username":github.get('user').data['login'],
            "post1":request.form["comment1"],
            "celebrity1":"Kendall",
            "post2":request.form["comment2"],
            "celebrity2":"Blake",
            "post3":request.form["comment3"],
            "celebrity3":"Emma"
            }
            collection.insert_one(thisdict)
            v1 = collection.find({"celebrity1":"Kendall"})
            v2 = collection.find({"celebrity2":"Blake"})
            v3 = collection.find({"celebrity3":"Emma"})

            formatted_posts1 = ""
            for post in v1:
                formatted_posts1 = formatted_posts1 + post["username"] + Markup(": ")+ post["post1"] + Markup("<br>")
            formatted_posts2 = ""
            for post in v2:
                formatted_posts2 = formatted_posts2 + post["username"] + Markup(": ")+ post["post2"] + Markup("<br>")
            formatted_posts3 = ""
            for post in v3:
                formatted_posts3 = formatted_posts3 + post["username"] + Markup(": ")+ post["post3"] + Markup("<br>")
            return render_template('page1.html', c1 = formatted_posts1, c2 = formatted_posts2, c3 = formatted_posts3)
        else:
            return render_template('message.html', message='Error: An empty comment was submitted. Please type something in and try again!')

collection = db["data"]

@github.tokengetter
def get_github_oauth_token():
    return session['github_token']


if __name__ == '__main__':
    app.run(debug=True)
