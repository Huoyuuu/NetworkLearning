'''
@Author   :   Huoyuuu + chatGPT
@File     :   DNS解析+GUI.py
@Version  :   1.0
@Contact  :   Huoyuuu@gmail.com
@License  :   MIT
@Time     :   23.2.11
@Desc     :   自动将域名解析为IP地址
'''

import dnslib
import socket
import tkinter as tk
from threading import Thread
from tqdm import tqdm

dns_list = ["114.114.114.114", "223.5.5.5", "180.76.76.76", "119.29.29.29", "117.50.11.11",
            "101.226.4.6", "123.125.81.6", "8.8.8.8", "208.67.222.222"]
ret_list = []
ip_list = []
timed_list = []
limited_time = 0.5


# 对单个dns服务器进行域名解析，并将结果存入列表内
def work_with_dnsserver(domain_name, dns_ip):
    request = dnslib.DNSRecord.question(domain_name)
    request_data = request.pack()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(limited_time)
    global ret_list, ip_list, timed_list
    try:
        # 通过UDP协议发送解析请求
        sock.sendto(request_data, (dns_ip, 53))
        response_data, address = sock.recvfrom(4096)
        response = dnslib.DNSRecord.parse(response_data)
        # 将结果存入列表内
        for rr in response.rr:
            ret_list.append(rr)
            if(rr.rdata not in ip_list):
                ip_list.append(str(rr.rdata))
    except Exception as e:
        timed_list.append(dns_ip)


# 打印结果
def print_result(domain_name):
    global ret_list, ip_list
    for ret in ret_list:
        output_text.insert(tk.END, ret)
        output_text.insert(tk.END, "\n")
    output_text.insert(tk.END, "\n")

    # 输出超时未响应的DNS服务器
    if(timed_list != []):
        output_text.insert(tk.END, f"设定倒计时为：{limited_time}s" + "\n")
        output_text.insert(tk.END, "超时DNS为" + "\n")
        for timed in timed_list:
            output_text.insert(tk.END, timed + "\n")
        output_text.insert(tk.END, "\n")

    # 输出解析结果（如果结果为纯数字，自动进行排序）
    output_text.insert(tk.END, domain_name + "解析结果为：")
    output_text.insert(tk.END, "\n")
    ip_list = list(set(ip_list))

    def no_lower_alpha():
        for item in ip_list:
            if(any(c.islower() for c in item)):
                return False
        return True

    if(no_lower_alpha()):
        ip_list.sort(key=lambda x: tuple(map(int, x.split('.'))))
    for ip in ip_list:
        output_text.insert(tk.END, ip)
        output_text.insert(tk.END, "\n")
    output_text.insert(tk.END, "\n")


# 初始化
def init():
    global ret_list, ip_list, timed_list
    ret_list = []
    ip_list = []
    timed_list = []
    output_text.delete("1.0", tk.END)


# 多线程获取解析结果，并输出到文本框内
def resolve_dns(domain_name):
    init()
    threads = []
    for dns_server in tqdm(dns_list):
        t = Thread(target=work_with_dnsserver, args=(domain_name, dns_server))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print_result(domain_name)
    output_text.see("end")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("DNS解析工具")

    # 顶部框架，包含输入框和按钮
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

    # 处理输入框
    input_entry = tk.Entry(top_frame, width=80, font=(
        "Arial", 10), justify="center")
    input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    input_entry.insert(tk.END, "qq.com")

    # 处理按钮
    get_input_button = tk.Button(
        top_frame, text="解析", command=lambda: resolve_dns(input_entry.get()))
    get_input_button.pack(side=tk.RIGHT, fill=tk.X)

    # 底部框架，包含用于输出结果的文本框
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # 处理文本框
    output_text = tk.Text(bottom_frame, wrap=tk.WORD)
    output_text.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
