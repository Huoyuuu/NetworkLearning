'''
@Author   :   Huoyuuu
@File     :   client.py
@Version  :   1.0
@Contact  :   Huoyuuu@gmail.com
@License  :   MIT
@Time     :   23.2.12
@Desc     :   作为多人聊天的服务器，多线程实现收发信息
'''

from socket import *
from threading import Thread

def new_connection():
    connectionSocket, addr = serverSocket.accept()
    user_name = connectionSocket.recv(1024).decode()
    connections.append(connectionSocket)
    while True:
        try:
            message = connectionSocket.recv(1024).decode()
            print(user_name + ":" + message)
            for socket in connections:
                socket.send((user_name + ":" + message.upper()).encode())
        except Exception as e:
            connections.remove(connectionSocket)
            connectionSocket, addr = serverSocket.accept()
            user_name = connectionSocket.recv(1024).decode()
            connections.append(connectionSocket)

if __name__ == "__main__":
    maxNum = 500
    serverPort = 12000
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("",serverPort))
    serverSocket.listen(maxNum * 2)
    connections = []
    threads = []
    for i in range(maxNum * 2):
        t = Thread(target=new_connection)
        t.start()