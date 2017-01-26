import sqlite3
import os
import datetime
import time

def addListing(user, listing, location, type, details):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%m-%d-%Y %H:%M")
    
    c.execute("INSERT INTO listings VALUES (?,?,?,?,?,?)",(listing,user,location,timestamp,type,details,))
    c.execute("SELECT rowid FROM listings WHERE user=? AND timestamp=?",(user,timestamp,))
    rowid = -1
    for x in c:
        rowid = x[0]
    db.commit()
    db.close()
    return rowid

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
    
def getImagesFromListing(id):
    data = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    a = c.execute("SELECT image FROM images WHERE id=?",(id,))
    for x in a:
        data.append(x[0])
        
    db.close()
    
    if not data:
        return ["noimage.jpg"]
    return data 

def addComment(id,user,comment):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%m-%d-%Y %H:%M")  
    c.execute("INSERT INTO comments VALUES (?,?,?,?)",(id,user,comment,timestamp,))
    
    db.commit()
    db.close()
    return 0

def getCommentsFor(id):
    ans = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 

    data = c.execute("SELECT * FROM comments WHERE id=?",(id,))
    for x in data:
        ans.append(x)
    db.close()
    return ans
    
def numComments(id):
    return len(getCommentsFor(id))
    
def addToWatchlist(user,id):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("INSERT INTO watchlist VALUES (?,?)",(user,id,))
    db.commit()
    db.close()
    return 0

def getListingInfoId(id):
    info = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("SELECT rowid, * FROM listings WHERE rowid=?",(id,))
    for x in c:
        image = getImagesFromListing(x[0])
        x = x + (image[0],numComments(x[0]),numLikes(x[0]),)
        
        
        info.append(x)   
    db.close()
    return info

def contain(text):
    data = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    text = "%" + text + "%"
    c.execute("SELECT rowid FROM listings WHERE listing LIKE ?",(text,))
    for x in c:
        data.append(getListingInfoId(x))
    db.close()
    return data

    
def getProducts():
    listings = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT ROWID, * FROM listings WHERE type='product'")
    for x in c:
        image = getImagesFromListing(x[0])
        x = x + (image[0],numComments(x[0]),numLikes(x[0]),)
        listings.append(x)   
    db.close()
    return listings
    
def getListingsP(user):
    info = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("SELECT ROWID, * FROM listings WHERE user=? and type='product'",(user,))
    for x in c:
        image = getImagesFromListing(x[0])
        x = x + (image[0],numComments(x[0]),numLikes(x[0]),)
        info.append(x)    
    db.close()
    return info
    
def getListingsS(user):
    info = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("SELECT rowid, * FROM listings WHERE user=? and type='service'",(user,))
    for x in c:
        image = getImagesFromListing(x[0])
        x = x + (image[0],numComments(x[0]),numLikes(x[0]),)
        info.append(x)    
    db.close()
    return info

def alreadyWatchlisted(user,id):
    info = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    data = c.execute("SELECT * FROM watchlist WHERE id=? AND user=?",(id,user,))
    for x in data:
        info.append(x)
    db.close()
    if len(info) > 0:
        return True
    else:
        return False
    
def getWatchlistP(user):
    watchlist = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("SELECT id FROM watchlist WHERE user=?",(user,))
    for x in c:
        info = getListingInfoId(x[0])[0]
        print (info)
        if info[5] == 'product':
            watchlist.append(info)
    db.close()
    return watchlist
    
def getWatchlistS(user):
    watchlist = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    c.execute("SELECT id FROM watchlist WHERE user=?",(user,))
    for x in c:
        info = getListingInfoId(x[0])[0]
        print (info)
        if info[5] == 'service':
            watchlist.append(info)
    db.close()
    return watchlist

def removeFromWatchlist(user,id):
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


def getServices():
    listings = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT ROWID, * FROM listings WHERE type='service'")
    for x in c:
        image = getImagesFromListing(x[0])
        x = x + (image[0],)
        listings.append(x)     
    db.close()
    return listings

def deleteAllListings():
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    c.execute("DELETE FROM listings")
    c.execute("DELETE FROM images")
    db.commit()
    db.close()
    
def getNextID():
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT max(rowid) FROM listings")
    for x in data:
        db.close()  
        return x[0] + 1


def likePost(user,id):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    if not alreadyLiked(user,id):
        c.execute("INSERT INTO likes VALUES (?,?)",(id,user,))
        db.commit()
        db.close()
    return 0
    
def unlikePost(user,id):
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    if alreadyLiked(user,id):
        c.execute("DELETE FROM likes WHERE id=? AND user=?",(id,user,))
        db.commit()
        db.close()
    return 0
    
def alreadyLiked(user,id):
    info = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    data = c.execute("SELECT * FROM likes WHERE id=? AND user=?",(id,user,))
    for x in data:
        info.append(x)
    db.close()
    
    if len(info) > 0:
        return True
    else:
        return False

def numLikes(id):
    info = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor() 
    data = c.execute("SELECT * FROM likes WHERE id=?",(id,))
    for x in data:
        info.append(x)
    db.close()
    return len(info)
    
    
if __name__ == '__main__':
    os.chdir('..')


   
#add user rating to listings
