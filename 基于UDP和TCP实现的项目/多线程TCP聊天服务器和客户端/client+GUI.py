'''
@Author   :   Huoyuuu
@File     :   client.py
@Version  :   1.0
@Contact  :   Huoyuuu@gmail.com
@License  :   MIT
@Time     :   23.2.12
@Desc     :   作为客户端连接服务器，可以收发信息，附带GUI界面
'''

from socket import *
from threading import Thread
import tkinter as tk

def get_message():
    while True:
        message = clientSocket.recv(1024).decode()
        if(message):
            output_text.insert(tk.END,message)
            output_text.insert(tk.END,"\n")
        else:
            return
    
if __name__ == "__main__":
    randomMsg = "18989b8dab2df405449c16cb0"
    serverName = "127.0.0.1"
    serverPort = 12000
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))

    user_name = input("输入用户名：")
    clientSocket.send(user_name.encode())

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
        top_frame, text="发送", command=lambda: clientSocket.send(input_entry.get().encode()))
    get_input_button.pack(side=tk.RIGHT, fill=tk.X)

    # 底部框架，包含用于输出结果的文本框
    bottom_frame = tk.Frame(root)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # 处理文本框
    output_text = tk.Text(bottom_frame,font=(
        "宋体", 12), wrap=tk.WORD)
    output_text.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
