from socket import *
server_name = "127.0.0.1"
server_port = 12000
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))
print()
print("客户端开始运行")
while True:
    message = input("输入内容：")
    client_socket.send(message.encode())
    if(message == "quit"):
        client_socket.close()
        print("客户端结束运行")
        print()
        break
    get_message = client_socket.recv(1024)
    print(get_message.decode())
