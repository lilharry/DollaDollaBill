from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import json
import urllib
from utils import listings, login

app = Flask(__name__)

@app.route('/')
def homepage():
    error = request.args.get('error') 
    success = request.args.get('success') 
    products = listings.getProducts()
    services = listings.getServices()
    #[rowid, listing, user, location, timestamp,type,details]
    #[0,     1,       2,    3,        4,        5,   6]
    return render_template("home.html",products=products, services=services,success=success,error=error)

@app.route('/authenticate/', methods=['POST'])
def authenticate():

    pw = request.form["pass"]
    un = request.form["user"]
    tp = request.form["action"]#login vs. register

    if tp == "register":
        regRet = login.register(un,pw)#returns an error/success message
        if regRet == 1:
            return redirect(url_for('homepage',success="You have registered"))
        else:
            return redirect(url_for('homepage',error=regRet))

    if tp == "login":
        text = login.login(un,pw)#error message
        if text == "":#if no error message, succesful go back home
            session["Username"] = un
            print('Username' not in session)
            return redirect(url_for('homepage',success="You have logged in"))
        return redirect(url_for('homepage',error=text))

    
@app.route('/results')
def results():
    #query = request.args.get('search')

    #if not query:
    #    return redirect(url_for("homepage"))
    #results = listings.search(query)    
    return render_template("results.html")#,results)
        

@app.route('/create/')
def create():
    return render_template("post.html")
        
@app.route('/profile/')
def myProfile():
    if 'Username' in session:
        return redirect(url_for('profile',username=session['Username']))
    else:
        return redirect(url_for('homepage',error="You must log in first"))
        
@app.route('/profile/<username>/')
def profile(username):
    if not login.duplicate(username):
        return redirect(url_for('homepage', error="No such user"))
    mp = listings.getListingsP(username)
    ms = listings.getListingsS(username)
    wp = listings.getWatchlistP(username)
    ws = listings.getWatchlistS(username)
    return render_template('profile.html',username=username,mp=mp,ms=ms,wp=wp,ws=ws)

@app.route('/listing/<id>/')
def listing(id):
    data = getListingInfoId(id)
    return render_template("listing.html",listing=data)

@app.route('/postitem/',methods=['POST'])
def post():
    user = session['Username']
    listing = request.form["listing"]
    location = request.form["location"]
    type = request.form["type"]
    details = request.form["details"]
    
    id = listings.addListing(user,listing,location,type,details)
    return render_template('upload.html',listing=listing,id=id)

@app.route('/logout/')
def logout():
    session.pop("Username")
    return redirect(url_for('homepage',success="You have successfully logged out"))
'''
@app.route("/postitem/")
def upload():
    target = os.path.join(APP_ROOT, 'static/')
    if not os.path.isdir(target):
        os.mkdir(target)

    files = request.files.getlist("file")
    i = 0

    for file in files:
        #print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        i += 1
        print i

    print os.listdir(os.path.join(APP_ROOT, 'uploaded/'))
    return render_template("confirm.html", title = "Almost There!", more = "Check if the emails correspond to the files:",
        filelist = os.listdir(os.path.join(APP_ROOT, 'uploaded/')), emails = tempList, mailingList = tempList, subject = tempsubject, msg_body = tempmsg_body)
        

def delete():
    files = os.listdir(os.path.join(APP_ROOT, 'uploaded/'))
    for file in files:
        print file
        print files
        os.remove(os.path.join(os.path.join(APP_ROOT, 'uploaded/'), file))

    files = os.listdir(os.path.join(APP_ROOT, 'uploaded/'))

    return (not files)
'''     

    
if __name__ == '__main__':
    if os.path.getsize("data/database.db") == 0:
        f = "data/database.db"
        db = sqlite3.connect(f, check_same_thread=False)
        c = db.cursor()
        print("Initializing database")
        c.execute("CREATE TABLE users (user TEXT, password TEXT)")
        c.execute("CREATE TABLE watchlist (user TEXT, id INTEGER, type TEXT)")
        c.execute("CREATE TABLE listings (listing TEXT, user TEXT, location TEXT, timestamp TEXT, type TEXT, details TEXT)")
        c.execute("CREATE TABLE images (id INTEGER, image TEXT)")
        c.execute("CREATE TABLE comments (id INTEGER, user TEXT, comment TEXT, timestamp TEXT)")
        db.commit()
        db.close()
    app.debug = True
    app.secret_key = '  \x43\xd2\x34\x92\x5b\x4a\x80\xfc\xc6\xb0\x0e\x45\xdd\x51\x36\xc0\xd2\x3a\x85\x42\x57\xbb\x61\xf2\x7b\xb6\xfc\x17\x3b\x1a\xda\x5b\x6d\x7d\x0a\xff\xd3\x6f\xfa\x7c\x1b\xa8\x0f\x7f\x53\x18\x8d\x91\x16\x81'
    app.run()
