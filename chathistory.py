import sqlite3
import time

def insert(uid,nick,msg):
    with sqlite3.connect('chathistory.db') as dbx:
        db=dbx.cursor()
        db.execute('INSERT INTO chat0 (id,nickname,message,timestamp) VALUES (?,?,?,?)',(uid,nick,msg,int(str(time.time()).replace('.',''))))
        # db.execute('INSERT INTO default VALUES (1,2,3,4)')
        db.close()
        dbx.commit()
        