'''
@Author   :   Huoyuuu
@File     :   server.py
@Version  :   1.0
@Contact  :   Huoyuuu@gmail.com
@License  :   MIT
@Time     :   23.2.12
@Desc     :   作为多人聊天的服务器，多线程实现收发信息
'''

from socket import *
from threading import Thread

# 与单个客户端进行交互
def new_connection():
    # 建立新的连接
    connection_socket, addr = server_socket.accept()
    user_name = connection_socket.recv(1024).decode()
    connections.append(connection_socket)
    while True:
        try:
            # 接收客户端信息
            message = connection_socket.recv(1024).decode()
            print(user_name + ":" + message)
            # 向所有客户端广播信息
            for socket in connections:
                socket.send((user_name + ":" + message.upper()).encode())
        except Exception as e:
            # 客户端关闭连接
            connections.remove(connection_socket)
            connection_socket, addr = server_socket.accept()
            user_name = connection_socket.recv(1024).decode()
            connections.append(connection_socket)

if __name__ == "__main__":
    # 建立与客户端交互的套接字
    max_connection_num = 500
    serverPort = 12000
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(("",serverPort))
    server_socket.listen(max_connection_num)
    connections = []
    threads = []
    for i in range(max_connection_num):
        t = Thread(target=new_connection)
        t.start()