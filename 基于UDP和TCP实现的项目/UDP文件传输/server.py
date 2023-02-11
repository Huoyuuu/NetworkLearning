from socket import *
from tqdm import tqdm
import json
import base64


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


if __name__ == "__main__":
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("服务器启动完毕")
    while True:
        new_packets = []
        length, addr = serverSocket.recvfrom(1024)
        length = int(length.decode())
        print("总长度为", length)
        for i in tqdm(range(length)):
            message, addr = serverSocket.recvfrom(2048)
            new_packets.append(json.loads(message.decode('utf-8')))
        new_packets = [
            [x[0], base64.b64decode(x[1].encode())] for x in new_packets]
        merge_packets_to_file(new_packets, "输出结果.jpg")
