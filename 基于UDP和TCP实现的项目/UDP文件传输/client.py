from socket import *
from tqdm import tqdm
import sys
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
    serverName = "127.0.0.1"
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    target = (serverName, serverPort)

    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = "示例文件.jpg"
    packets = split_file_into_packets(file_name, 1024)
    client_SHA_256 = sha256_hash_of_file(file_name)
    clientSocket.sendto(str(len(packets)).encode(), target)
    clientSocket.sendto(file_name.encode(), target)
    clientSocket.sendto(client_SHA_256.encode(), target)
    print(f"总长度为{len(packets)}")
    print(f"文件名为{file_name}")
    encoded_byte_array = [(x[0], base64.b64encode(x[1]).decode())
                          for x in packets]
    for packet in tqdm(encoded_byte_array):
        clientSocket.sendto(json.dumps(packet).encode(
            'utf-8'), target)
    server_SHA_256, addr = clientSocket.recvfrom(1024)
    server_SHA_256 = server_SHA_256.decode()
    check_SHA_256(server_SHA_256, client_SHA_256)
    clientSocket.close()
