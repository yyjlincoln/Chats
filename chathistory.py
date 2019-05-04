import sqlite3
import time

def insert(uid,nick,msg):
    with sqlite3.connect('chathistory.db') as dbx:
        db=dbx.cursor()
        db.execute('INSERT INTO default VALUES (?,?,?,?)',(uid,nick,msg,int(str(time.time()).replace('.',''))))
        db.close()
        dbx.commit()
        