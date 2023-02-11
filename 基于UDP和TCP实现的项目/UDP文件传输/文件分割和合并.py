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


packets = split_file_into_packets("示例文件.jpg", 30)
print(f"分出{len(packets)}个包")
merge_packets_to_file(packets, "输出结果.jpg")
