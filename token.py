import sqlite3
import time
import random
import secrets

dbx=sqlite3.connect('token.db')
db=dbx.cursor()

def newToken(id=None):
    token=secrets.token_urlsafe(64)
    try:
        db.execute('INSERT INTO token (id,token,created) VALUES (?,?,?)',(id,token,int(str(time.time()).replace('.',''))))
        dbx.commit()
        return token
    except sqlite3.IntegrityError:
        try:
            db.execute('UPDATE token SET token=?,created=? WHERE id=?',(token,int(str(time.time()).replace('.','')),id))
            dbx.commit()
            return token
        except:
            return False
    return False

def validateToken(id,token):
    db.execute('SELECT token FROM token WHERE id=?',(id,))
    x=db.fetchone()
    if len(x)==0:
        print('1')
        return False
    if x[0]==token:
        return True
    return False
