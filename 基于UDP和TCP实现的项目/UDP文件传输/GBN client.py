import socket
import json
import base64
import hashlib
import sys
from tqdm import tqdm
from time import sleep


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


def send_packets(s, packets, serverName, serverPort):
    count = 0
    for packet in tqdm(packets):
        while True:
            s.sendto(json.dumps([packet[0], base64.b64encode(
                packet[1]).decode()]).encode(), (serverName, serverPort))
            ack, addr = s.recvfrom(2048)
            if(int(ack.decode()) == packet[0]):
                break
            else:
                count += 1
                print(f"第{packet[0]}个包出现问题，进行重传，重传总数为{count}")


def check_SHA_256(server_SHA_256, client_SHA_256):
    print(f"发送端SHA-256为{client_SHA_256}")
    print(f"接收端SHA-256为{server_SHA_256}")
    if(client_SHA_256 == server_SHA_256):
        print("传输无误")
    else:
        print("传输结果异常")


def send_file(file, serverName, serverPort):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_size = 2048
    packets = split_file_into_packets(file, packet_size)
    length = len(packets)
    s.sendto(str(length).encode(), (serverName, serverPort))
    s.sendto(file.encode(), (serverName, serverPort))
    client_SHA_256 = sha256_hash_of_file(file)
    s.sendto(client_SHA_256.encode(), (serverName, serverPort))
    send_packets(s, packets, serverName, serverPort)
    sleep(0.1)
    server_SHA_256, addr = s.recvfrom(2048)
    server_SHA_256 = server_SHA_256.decode()
    check_SHA_256(server_SHA_256, client_SHA_256)
    s.close()


if __name__ == "__main__":
    serverName = "192.168.91.131"
    serverPort = 12000
    if(len(sys.argv) >= 2):
        file = sys.argv[2]
    else:
        file = "软技能 代码之外的生存指南.pdf"
    send_file(file, serverName, serverPort)
