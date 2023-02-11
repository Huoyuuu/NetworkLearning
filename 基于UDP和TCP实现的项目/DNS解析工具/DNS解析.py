'''
@Author   :   Huoyuuu + chatGPT
@File     :   DNS解析.py
@Version  :   1.0
@Contact  :   Huoyuuu@gmail.com
@License  :   MIT
@Time     :   23.2.11
@Desc     :   自动将域名解析为IP地址
'''

import dnslib
import socket
from threading import Thread
from tqdm import tqdm

dns_list = ["114.114.114.114", "223.5.5.5", "180.76.76.76", "119.29.29.29", "1.2.4.8", "117.50.11.11",
            "101.226.4.6", "123.125.81.6", "8.8.8.8", "208.67.222.222"]
ret_list = []
ip_list = []
timed_list = []
limited_time = 0.5


def work_with_dnsserver(domain_name, dns_ip):
    request = dnslib.DNSRecord.question(domain_name)
    request_data = request.pack()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(limited_time)
    global ret_list, ip_list, timed_list
    try:
        sock.sendto(request_data, (dns_ip, 53))
        response_data, address = sock.recvfrom(4096)
        response = dnslib.DNSRecord.parse(response_data)
        for rr in response.rr:
            ret_list.append(rr)
            if(rr.rdata not in ip_list):
                ip_list.append(str(rr.rdata))
    except Exception as e:
        timed_list.append(dns_ip)


def print_result(domain_name):
    global ret_list, ip_list
    for ret in ret_list:
        print(ret)
    print()

    if(timed_list != []):
        print(f"设定倒计时为：{limited_time}s")
        print("超时DNS为")
        for timed in timed_list:
            print(timed)
        print()

    print(domain_name, "对应IP为")
    ip_list = list(set(ip_list))

    def no_lower_alpha():
        for item in ip_list:
            if(any(c.islower() for c in item)):
                return False
        return True

    if(no_lower_alpha()):
        ip_list.sort(key=lambda x: tuple(map(int, x.split('.'))))
    for ip in ip_list:
        print(ip)
    print()


def resolve_dns(domain_name):
    domain_name = domain_name.removeprefix("https://")
    domain_name = domain_name.removeprefix("http://")
    domain_name = domain_name.split('/')[0]
    threads = []
    for dns_server in tqdm(dns_list):
        t = Thread(target=work_with_dnsserver, args=(domain_name, dns_server))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print_result(domain_name)


if __name__ == "__main__":
    domain_name = input("Enter the domain name: ")
    resolve_dns(domain_name)
