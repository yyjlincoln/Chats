import os
import sys
import math
import socket
import threading
import getpass
import urllib.parse
import json
import base64
import netr

msgUnread=[]

# All Exceptions
class HostingException(BaseException):
    def __init__(self,r,errcode):
        return

# Launch Listening Thread
class WebHostWaiting(threading.Thread):
    def __init__(self,soc):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.setName('WebHosting Accepting - MAIN')
        self.soc=soc
    
    def run(self):
        try:
            soc=self.soc
            if not soc:
                raise HostingException('No socket connection is provided',-1)
            while True:
                try:
                    sx,addr=soc.accept()
                    t=WebHostAccepted(sx,addr)
                    t.start()
                except:
                    pass
        except:
            pass

class WebHostAccepted(threading.Thread):
    def __init__(self,sx,addr):
        threading.Thread.__init__(self)
        self.sx=sx
        self.addr=addr
        self.setDaemon(True)
        self.setName('WebHosting Accepted - '+addr[0]+':'+str(addr[1]))

    def run(self):
        try:
            sx=self.sx
            addr=self.addr
            d=sx.recv(204800000)
            p=parseAddr(d)
            if p:
                ds=getData(p)
                if ds!=False:
                    sx.send(b'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\r\n\r\n'+ds)
                else:
                    sx.send(b'HTTP/1.1 404 Not Found\nAccess-Control-Allow-Origin: *\r\n\r\nNot Found.')
            else:
                sx.send(b'HTTP/1.1 500 Bad Request\nAccess-Control-Allow-Origin: *\r\n\r\nBad HTTP Request.')
            sx.shutdown(socket.SHUT_RDWR)
            sx.close()
        except Exception as e:
            print(e)
            pass

def msgrecv(nickname,id,message,timestamp):
    global msgUnread
    msgUnread.append({'id':id,'nickname':nickname,'message':message,'timestamp':timestamp})

def main():
    # Host on Localhost
    s=socket.socket()
    s.bind(('localhost',8099))
    s.listen(10)
    W=WebHostWaiting(s)
    W.start()
    W.join()

def parseAddr(r):
    try:
        r=r.decode()
        r=r.split('\r\n')
        r=r[0].split(' ')[1]
        return r
    except:
        pass

def getData(r):
    try:
        if r=='/':
            r='/index.html'
        if r[:6]=='/$api/':
            return api(r[6:])
        else:
            try:
                with open('./web/'+r[1:],'rb') as f:
                    return f.read()
            except Exception as e:
                print(e)
                return False
    except Exception as e:
        print('1'+e)
        return False

def api(d):
    try:
        if d[:5]=='init/':
            dd=d[5:].split('/')
            if len(dd)<4:
                return jsond('Init field not completed', False, -5005)
            try:
                rst=netr.init((dd[0],int(dd[1])),(dd[2],dd[3]),msghand=msgrecv)
                if rst <0:
                    return jsond('Init failed',False,int(rst))
            except:
                return jsond('Init server port should be int',False,-5999)
            return jsond('Init Success.')
        
        if d[:5]=='send/':
            commandB64=d[5:]
            commandB64=urllib.parse.unquote(commandB64)
            try:
                command=base64.b64decode(commandB64)
            except:
                return jsond('Failed to parse b64',False,-5001)
            print(command)
            r=command
            
            try:
                rj=json.loads(r)
            except:
                return jsond('Failed to parse json',False,-5002)
            
            if 'msg' not in rj:
                return jsond('No msg is decleared; Json format error?',False,-5003)

            #Got Command
            rst=netr.sendmsg(rj['msg'])
            if rst>=0:
                return jsond('Message sent')
            else:
                return jsond('Message send failed',False,int(rst))
        if d=='initstat':
            return jsond('<Status>',netr.initok(),code=0)
        if d=='getusername':
            try:
                return jsond(netr.nickname,netr.initok(),code=0)
            except:
                return jsond('<Uninitialized>',False,-5998)
        if d=='getid':
            try:
                return jsond(netr.ID,netr.initok(),code=0)
            except:
                return jsond(-1,False,-5998)
        if d=='getmsg':
            c=[]
            if not netr.initok():
                return jsond('<Session Expired>',False,-1)
            if len(msgUnread)!=0:
                for x in range(len(msgUnread)):
                    c.append(msgUnread[0])
                    msgUnread.pop(0)
                return jsond(c,True,0)
            return jsond(c,False,0)
        return jsond('Invalid operation',False,-5000)
    except Exception as e:
        return jsond('Unknown error occured, raw error information presented.'+str(e),False,-5999)

def jsond(message='success',success=True,code=0,**kw):
    c={
        'success':success,
        'code':code,
        'message':message
    }
    for x in kw:
        c[x]=kw[x]
    try:
        r=json.dumps(c)
    except:
        return False
    return r.encode()

main()