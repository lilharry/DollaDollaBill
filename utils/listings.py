import sqlite3
import os
import datetime
import time

def addListing(user, listing, location, type, details):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%m-%d-%Y %H:%M")
    
    c.execute("INSERT INTO listings VALUES (?,?,?,?,?,?)",(listing,user,location,timestamp,type,details))
    
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

def addImageToListing(id,image):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("INSERT INTO images VALUES (?,?)",(id,image,))
    db.commit()
    db.close()
    return 0

def addComment(id,user,comment):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    
    
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%m-%d-%Y %H:%M")  
    c.execute("INSERT INTO comments VALUES (?,?,?,?)",(id,user,comment,timestamp,))
    
    db.commit()
    db.close()
    return 0

def addToWatchlist(user,id):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("INSERT INTO watchlist VALUES (?,?)",(user,id,))
    db.commit()
    db.close()
    return 0

def getWatchlist(user):
    watchlist = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("SELECT id FROM watchlist WHERE user=?",(user,))
    for x in c:
        watchlist.append(getListingInfo(x[0]))
    db.close()
    return watchlist
    

def getListingInfo(listing):
    info = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("SELECT * FROM listings WHERE listing=?",(listing,))
    for x in c:
        info.append(x)
    db.close()
    return info

def getListingInfoId(id):
    info = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("SELECT * FROM listings WHERE rowid=?",(id,))
    for x in c:
        info.append(x)
    db.close()
    return info

def removeWatchlist(user,id):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("DELETE FROM watchlist WHERE user=? AND id=?",(user,id,))
    db.commit()
    db.close()

def clearWatchlist(user):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("DELETE FROM watchlist WHERE user=?", (user,))
    db.commit()
    db.close()

    
def getProducts():
    listings = []
    
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT ROWID, * FROM listings WHERE type='product'")
    for x in c:
        listings.append(x)   
    db.close()
    return listings

def getServices():
    listings = []
    
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT ROWID, * FROM listings WHERE type='service'")
    for x in c:
        listings.append(x)   
    db.close()
    return listings

    
if __name__ == '__main__':
    os.chdir('..')
    addListing('john','jordans','brooklyn','product','hello')
    addListing('yeeee kaii','smartwatch','canada','product','hello')
    
    print(getProducts())
   
#add user rating to listings
    
    
    
    