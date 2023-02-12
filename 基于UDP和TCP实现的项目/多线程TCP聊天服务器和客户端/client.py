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

def get_message():
    while True:
        message = clientSocket.recv(1024).decode()
        if(message):
            print(message)
        else:
            return

def send_message():
    while True:
        message = input()
        clientSocket.send(message.encode())
        
serverName = "127.0.0.1"
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

user_name = input("输入用户名：")
clientSocket.send(user_name.encode())

t1 = Thread(target = get_message)
t2 = Thread(target = send_message)
t1.start()
t2.start()

