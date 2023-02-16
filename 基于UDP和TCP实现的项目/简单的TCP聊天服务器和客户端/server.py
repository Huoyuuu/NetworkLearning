from socket import *
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)
print("服务器开始运行")
connection_socket, addr = server_socket.accept()
while True:
    try:
        sentence = connection_socket.recv(1024).decode()
        sentence = str(addr[0]) + ":" + str(addr[1]) + ": " + sentence
        connection_socket.send(sentence.encode())
        print(sentence)
    except:
        print("客户端已断开连接")
        break
