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
    serverName = "127.0.0.1"
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    packets = split_file_into_packets('示例文件.jpg', 1024)
    clientSocket.sendto(str(len(packets)).encode(), (serverName, serverPort))
    print("总长度为", len(packets))
    encoded_byte_array = [(x[0], base64.b64encode(x[1]).decode())
                          for x in packets]
    for packet in tqdm(encoded_byte_array):
        clientSocket.sendto(json.dumps(packet).encode(
            'utf-8'), (serverName, serverPort))
    clientSocket.close()
