import os
import sys
import math
import socket
import threading
import getpass
import urllib.parse

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
                with open('./webmgr/'+r[1:],'rb') as f:
                    return f.read()
            except Exception as e:
                print(e)
                return False
    except Exception as e:
        print('1'+e)
        return False

def api(d):
    try:
        if d=='init':
            return b'''
            ====================================
            You have successfully connected to:
            '''+getpass.getuser().encode()+b'''
            ====================================
            '''
        
        if d[:5]=='send/':
            command=d[5:]
            command=urllib.parse.unquote(command)
            print(command)
            z=os.system(command+' >log.log 2>log.err')
            with open('log.log','r') as f:
                r=f.read()
            with open('log.err','r') as f:
                r=r+f.read()
            if r=='':
                r='<No output>'
                return r.encode()
            return r.encode()
        return b'Unrec'
    except:
        return b'Failed to exec.'

main()