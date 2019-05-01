import socket
import os
import sys
import threading
import time
import json

servaddr = ('localhost', 8088)
s = socket.socket()
token = ''
sign = ''
authstat = False
connectstat = False
xauth = ()
msgrecv=print

def sendmsg(msg):
    global token
    c = {
        'timestamp': time.time(),
        'operation': 'msgsend',
        'token': token,
        'msg': msg
    }
    d=socket.socket()
    try:
        d.connect(servaddr)
    except:
        return False
    try:
        d.send(json.dumps(c).encode())
    except:
        return False
    din = json.loads(d.recv(2048).decode())
    if 'success' in din:
        if din['success'] == True:
            return True
        else:
            return False
    else:
        return False


def init(serv=('localhost', 8088), auth=('user', 'pass'),msghand=None):
    global servaddr, s, connectstat, xauth, msgrecv
    s=socket.socket()
    if msghand:
        msgrecv=msghand

    servaddr = serv
    try:
        s.connect(servaddr)
    except:
        s = socket.socket()
        return False
    print(authorize(auth))
    if not authorize(auth):
        s = socket.socket()
        return False
    connectstat = True
    xauth = auth
    msgf = MsgFetch()
    msgf.start()
    return True


def authorize(auth):
    global sign, token, authstat
    try:
        # [TODO]
        print(auth)
        if auth[0] == 'user' and auth[1] == 'pass':
            token = '123456'
            sign = '654321'
            authstat = True
            return True
        return False
    except:
        return False



class MsgFetch(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.setName('Msg Fetch')

    def run(self):
        global s
        while True:
            try:
                d=s.recv(204800).decode()
                if d=='heartbeat':
                    continue
                jback=json.loads(d)
                if not 'msgtype' in jback:
                    print('Msgtype not found')
                    continue
                if jback['msgtype']=='msg':
                    if 'msg' not in jback or 'id' not in jback or 'nickname' not in jback:
                        print('msg err')
                        continue
                    else:
                        msgrecv(jback['nickname'],jback['id'],jback['msg'])
            except:
                netwreset()
                return

def netwreset():
    global s, authstat, connectstat, token, sign
    s.close()
    s=socket.socket()
    connectstat=False
    authstat=False
    token=''
    sign=''
    offline_reconnect()
    if init(serv=servaddr,auth=xauth):
        offline_reconnect_success()
    else:
        offline_reconnect_failed()

def orc():
    print('You are now offline. Reconnecting...')

def orcs():
    print('You are now back online.')

def orcf():
    print('Unable to reconnect.')

offline_reconnect=orc
offline_reconnect_failed=orcf
offline_reconnect_success=orcs


#class Heartbeat(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.setDaemon(True)
#         self.setName('Heartbeat Thread')

#     def run(self):
#         global s
#         while True:
#             time.sleep(20)
#             try:
#                 s.send(b'heartbeat')
#                 z = s.recv(2048)
#                 if z == b'heartbeat':
#                     continue
#             except:
#                 netwreset()
#                 return
