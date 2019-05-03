import os
import sys
import threading
import time
import socket

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
            d=sx.recv(204800000).decode()


            #[TODO]

            

            sx.shutdown(socket.SHUT_RDWR)
            sx.close()
        except Exception as e:
            print(e)
            pass

def main():
    s=socket.socket()
    s.bind(('localhost',8088))
    s.listen(10)
    hosting=WebHostWaiting(s)
    hosting.start()
    hosting.join()

main()


# import socket
# import json

# s=socket.socket()
# s.bind(('',8088))
# s.listen(10)
# while True:
#     try:
#         sx,addr=s.accept()
#         d=sx.recv(2048).decode()
#         print(d)
#         e=json.loads(d)
#         print(e)
#         sx.send(json.dumps({'success':True}).encode())
#         sx.close()
#     except:
#         continue