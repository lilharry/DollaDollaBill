from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import json
import urllib,urllib2

app = Flask(__name__)

@app.route('/')
def homepage():
    error = request.args.get('error') 
    success = request.args.get('success') 
    
    return render_template("home.html",success=success,error=error)

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
        

@app.route('/create/<id>')
def create(id):
    return render_template("post.html")
        

@app.route('/listing/<id>/')
def listing(id):
    return render_template("listing.html");
        
    
if __name__ == '__main__':
    if os.path.getsize("data/database.db") == 0:
        f = "data/database.db"
        db = sqlite3.connect(f, check_same_thread=False)
        c = db.cursor()
        print "Initializing database"
        c.execute("CREATE TABLE users (user TEXT, password TEXT)")
        c.execute("CREATE TABLE watchlist (user TEXT, game INTEGER)")
        c.execute("CREATE TABLE listings (id INTEGER, listing TEXT, user TEXT, location TEXT, timestamp TEXT, type TEXT)")
        c.execute("CREATE TABLE images (id INTEGER, image TEXT)")
        c.execute("CREATE TABLE comments (id INTEGER, user TEXT, comment TEXT, timestamp TEXT)")
        db.commit()
        db.close()
    app.debug = True
    app.secret_key = '  \x43\xd2\x34\x92\x5b\x4a\x80\xfc\xc6\xb0\x0e\x45\xdd\x51\x36\xc0\xd2\x3a\x85\x42\x57\xbb\x61\xf2\x7b\xb6\xfc\x17\x3b\x1a\xda\x5b\x6d\x7d\x0a\xff\xd3\x6f\xfa\x7c\x1b\xa8\x0f\x7f\x53\x18\x8d\x91\x16\x81'
    app.run()