from socket import *
from tqdm import tqdm
import json
import base64
import hashlib


def sha256_hash_of_file(filename):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()


def split_file_into_packets(file, packet_size):
    packets = []
    count = 0
    with open(file, 'rb') as f:
        while True:
            packet = f.read(packet_size)
            if(packet):
                packets.append([count, packet])
                count += 1
            else:
                break
    return packets


def merge_packets_to_file(packets, file):
    packets = sorted(packets, key=lambda x: x[0])
    with open(file, 'wb') as f:
        for packet in packets:
            f.write(packet[1])


def check_SHA_256(server_SHA_256, client_SHA_256):
    print(f"发送端SHA-256为{client_SHA_256}")
    print(f"接收端SHA-256为{server_SHA_256}")
    if(client_SHA_256 == server_SHA_256):
        print("传输无误")
    else:
        print("传输结果异常")


if __name__ == "__main__":
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("服务器启动完毕")
    while True:
        new_packets = []
        length, addr = serverSocket.recvfrom(1024)
        file_name, addr = serverSocket.recvfrom(1024)
        client_SHA_256, addr = serverSocket.recvfrom(1024)
        length = int(length.decode())
        file_name = file_name.decode()
        client_SHA_256 = client_SHA_256.decode()
        print(f"总长度为{length}")
        print(f"文件名为{file_name}")
        for i in tqdm(range(length)):
            message, addr = serverSocket.recvfrom(2048)
            new_packets.append(json.loads(message.decode('utf-8')))
        new_packets = [
            [x[0], base64.b64decode(x[1].encode())] for x in new_packets]
        merge_packets_to_file(new_packets, "接受到的" + file_name)

        server_SHA_256 = sha256_hash_of_file("接受到的" + file_name)
        serverSocket.sendto(server_SHA_256.encode(), addr)
        check_SHA_256(server_SHA_256, client_SHA_256)
