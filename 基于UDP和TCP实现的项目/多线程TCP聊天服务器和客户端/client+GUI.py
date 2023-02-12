'''
@Author   :   Huoyuuu
@File     :   client+GUI.py
@Version  :   1.0
@Contact  :   Huoyuuu@gmail.com
@License  :   MIT
@Time     :   23.2.12
@Desc     :   作为客户端连接服务器，可以收发信息，附带GUI界面
'''

from socket import *
from threading import Thread
import tkinter as tk

# 接收信息
def get_message():
    while True:
        message = client_socket.recv(1024).decode()
        if(message):
            output_text.insert(tk.END,message)
            output_text.insert(tk.END,"\n")
        else:
            return
    
if __name__ == "__main__":
    # 建立和服务器交互的套接字
    server_name = "127.0.0.1"
    server_port = 12000
    client_socket = socket(AF_INET,SOCK_STREAM)
    client_socket.connect((server_name,server_port))

    # 输入用户名
    user_name = input("输入用户名：")
    client_socket.send(user_name.encode())

    # 建立接收信息的线程
    # 发送信息由发送按钮负责完成，每此点击“发送”后发送一条信息。
    t = Thread(target = get_message)
    t.start()
    
    root = tk.Tk()
    root.title(user_name)

    # 顶部框架，包含输入框和按钮
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X, expand=True)

    # 处理输入框
    input_entry = tk.Entry(top_frame, width=80, font=(
        "宋体", 12), justify="center")
    input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    input_entry.insert(tk.END, "你好啊")

    # 处理按钮
    get_input_button = tk.Button(
        top_frame, text="发送", command=lambda: client_socket.send(input_entry.get().encode()))
    get_input_button.pack(side=tk.RIGHT, fill=tk.X)

    # 底部框架，包含用于输出结果的文本框
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # 处理文本框
    output_text = tk.Text(bottom_frame,font=(
        "宋体", 12), wrap=tk.WORD)
    output_text.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
