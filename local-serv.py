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
            d=sx.recv(2048)
            p=parseAddr(d)
            if p:
                ds=getData(p)
                if ds!=False:
                    sx.send(b'HTTP/1.1 200 OK\r\n\r\n'+ds)
                else:
                    sx.send(b'HTTP/1.1 404 Not Found\r\n\r\nNot Found.')
            else:
                sx.send(b'HTTP/1.1 500 Bad Request\r\n\r\nBad HTTP Request.')
            sx.shutdown(socket.SHUT_RDWR)
            sx.close()
        except Exception as e:
            print(e)
            pass



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
    except Exception as e:
        print('Err',e)

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
            if not netr.init((dd[0],dd[1]),(dd[2],dd[3])):
                return jsond('Init failed, check your address and login.',False,-5006)
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
            if netr.sendmsg(rj['msg']):
                return jsond('Message sent')
            else:
                return jsond('Message send failed',False,-5006)
        return jsond('Invalid operation',False,-5000)
    except Exception as e:
        return jsond('Unknown error occured, raw error information presented.\n'+e,False,-5999)

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