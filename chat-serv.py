import socket
import json

s=socket.socket()
s.bind(('',8088))
s.listen(10)
while True:
    try:
        sx,addr=s.accept()
        d=sx.recv(2048).decode()
        print(d)
        e=json.loads(d)
        print(e)
        sx.send(json.dumps({'success':True}).encode())
    except:
        continue