'''
@Author   :   Huoyuuu
@File     :   client.py
@Version  :   1.0
@Contact  :   Huoyuuu@gmail.com
@License  :   MIT
@Time     :   23.2.12
@Desc     :   作为客户端连接服务器，可以收发信息，无GUI界面
'''

from socket import *
from threading import Thread

# 接收信息
def get_message():
    while True:
        message = client_socket.recv(1024).decode()
        if(message):
            print(message)
        else:
            return

# 发送信息
def send_message():
    while True:
        message = input()
        client_socket.send(message.encode())

if __name__ == "__main__":
    # 建立和服务器交互的套接字
    server_name = "127.0.0.1"
    server_port = 12000
    client_socket = socket(AF_INET,SOCK_STREAM)
    client_socket.connect((server_name,server_port))

    # 输入用户名
    user_name = input("输入用户名：")
    client_socket.send(user_name.encode())

    # 两条线程分别用于接收信息和发送信息
    t1 = Thread(target = get_message)
    t2 = Thread(target = send_message)
    t1.start()
    t2.start()