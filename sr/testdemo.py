import socket
import time
import json

def tcpClient():
    host = "localhost"
    port = 5011
    dirct = {}
    s1 = socket.socket()
    s1.settimeout(1)
    s1.connect((host, 5011))
    dirct['type'] = "move2safe"
    message = json.dumps(dirct)
    def run(s1):
        s1.send(message.encode())
        try:
            s1.recv(1024)
        except:
            return run(s1)
    run(s1)
    # while True:
    #     time.sleep(2)

if __name__ == '__main__':
    tcpClient()