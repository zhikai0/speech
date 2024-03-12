import socket
import threading
import json
import time
# 创建 socket 对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
# 绑定端口号
s.bind((host, 5012))
# 设置最大连接数，超过后排队
s.listen(50)


def socket_receive(conn,addr):
    count = 0
    dircy = {}
    # 接受消息
    while True:
        data = conn.recv(1024)
        if not data:
            print("连接断开")          
            break
        print("收到消息:", data.decode())
        conn.send(data)

def test():
    while True:
        conn, addr = s.accept()
        print("连接地址:",addr)
        threading.Thread(target=socket_receive, args=(conn,addr)).start()

if __name__=="__main__":
    test()




