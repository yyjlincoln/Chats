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
    if not initok():
        return -1
    c = {
        'timestamp': time.time(),
        'operation': 'msgsend',
        'token': token,
        'msg': msg,
        'nickname': nickname,
        'id': ID,
    }
    d=socket.socket()
    try:
        d.connect(servaddr)
    except:
        return -5887
    try:
        d.send(json.dumps(c).encode())
    except:
        return -5886
    try:
        din = json.loads(d.recv(2048).decode())
    except:
        return -5888
    if 'success' in din:
        if din['success'] == True:
            return True
        else:
            return -1
    else:
        return -5999

def initok():
    return (connectstat&authstat)

def init(serv=('localhost', 8088), auth=('user', 'pass'),msghand=None):
    global servaddr, s, connectstat, authstat, xauth, msgrecv, ID, token, nickname
    s=socket.socket()
    if msghand:
        msgrecv=msghand

    servaddr = serv
    try:
        s.connect(servaddr)
    except:
        s = socket.socket()
        return -5887
    # print(authorize(auth))
    # if not authorize(auth):
    #     s = socket.socket()
    #     return -1
    try:
        s.send(json.dumps({
            'operation':'msgregister',
            'msg':'<msgregister>,',
            'email':auth[0],
            'password':auth[1]
        }).encode())
        d=s.recv(2048).decode()
        print(d)
        d=json.loads(d)
        if d['success']==True:
            token=d['token']
            ID=d['id']
            nickname=d['nickname']
            authstat=True
        else:
            s=socket.socket()
            return -1
    except:
        s=socket.socket()
        return -5999
    xauth = auth
    msgf = MsgFetch(auth)
    msgf.start()
    connectstat = True
    return 0


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
    def __init__(self,auth):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.setName('Msg Fetch')
        self.auth=auth

    def run(self):
        global s
        while True:
            try:
                print('MsgAwaits')
                d=s.recv(204800).decode()
                if d==b'':
                    raise Exception('Connection Reset')
                if d=='heartbeat':
                    continue
                try:
                   jback=json.loads(d)
                except:
                    print('JSON parse failed')
                    continue
                if not 'msgtype' in jback:
                    print('Msgtype not found')
                    continue
                if jback['msgtype']=='msg':
                    if 'msg' not in jback or 'id' not in jback or 'nickname' not in jback or 'timestamp' not in jback:
                        print('msg err')
                        continue
                    else:
                        msgrecv(jback['nickname'],jback['id'],jback['msg'],jback['timestamp'])
            except:
                netwreset()
                return
# def getusername():
#     return xauth[0]

def netwreset():
    global s, authstat, connectstat, token, sign
    s.close()
    s=socket.socket()
    connectstat=False
    authstat=False
    token=''
    sign=''
    offline_reconnect()
    if init(serv=servaddr,auth=xauth)>=0:
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
