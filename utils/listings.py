import sqlite3
import os
import datetime


def addListing(user, listing, location, type):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    
    timestamp = now.strftime("%m-%d-%Y %H:%M")
    
    c.execute("INSERT INTO listings VALUES (?,?,?,?,?)",(listing,user,location,timestamp,type,))
    
    db.commit()
    db.close()
    return 0

def removeListing(id):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("DELETE FROM listings WHERE rowid=?",(id,))
    
    db.commit()
    db.close()
    return 0