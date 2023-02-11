from socket import *
serverName = "127.0.0.1"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print()
print("客户端开始运行")
while True:
    message = input("输入内容：")
    clientSocket.send(message.encode())
    if(message == "quit"):
        clientSocket.close()
        print("客户端结束运行")
        print()
        break
    getMessage = clientSocket.recv(1024)
    print(getMessage.decode())
