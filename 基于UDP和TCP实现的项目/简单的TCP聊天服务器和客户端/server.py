from socket import *
serverName = "127.0.0.1"
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("服务器开始运行")
connectionSocket, addr = serverSocket.accept()
while True:
    sentence = connectionSocket.recv(1024).decode()
    sentence = str(addr[0]) + ":" + str(addr[1]) + ": " + sentence
    connectionSocket.send(sentence.encode())
    print(sentence)
