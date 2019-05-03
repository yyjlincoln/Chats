import sqlite3
import time

dbx=sqlite3.connect('userdata.db')
db=dbx.cursor()

def getNickName(id=None,email=None):
    if id:
        db.execute('SELECT nickname FROM userinfo WHERE id=?',(id,))
    elif email:
        db.execute('SELECT nickname FROM userinfo WHERE email=?',(email,))
    else:
        return False
    try:
        return db.fetchone()[0]
    except:
        return False

def getSaltedPassword(id=None,email=None):
    if id:
        db.execute('SELECT password FROM userinfo WHERE id=?',(id,))
    elif email:
        db.execute('SELECT password FROM userinfo WHERE email=?',(email,))
    else:
        return False
    try:
        return db.fetchone()[0]
    except:
        return False

def newUser(email,nickname,password):
    try:
        db.execute('INSERT INTO userinfo VALUES (?,?,?,?)',(int(str(time.time()).replace('.','')),email,nickname,password))
    except sqlite3.IntegrityError:
        return False
    dbx.commit()
    return True

def updatePassword(newpassword,id=None,email=None):
    try:
        if id:
            db.execute('UPDATE userinfo SET password=12345 WHERE id=?',(newpassword,id))
        elif email:
            db.execute('UPDATE userinfo SET password=? WHERE email=?',(newpassword,email))
        else:
            return False
        dbx.commit()
        return True
    except:
        return False

def getEmail(id):
    try:
        db.execute('SELECT email FROM userinfo WHERE id=?',(id,))
        return db.fetchone()[0]
    except:
        return False

def getID(email):
    try:
        db.execute('SELECT id FROM userinfo WHERE email=?',(email,))
        return db.fetchone()[0]
    except:
        return False

