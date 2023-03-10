## 使用 UDP 协议实现文件传输

### 处理问题
- 数据包丢失/未能按序抵达
- 数据包的错误检测和纠正
- 控制传输速度（输出方根据接收方的缓存大小和接收速率调整传输速率，避免接收方缓存区溢出）
- 拥塞控制（网络拥塞情况下，输出方调整传输速率。注意上一条区分，前面处理接收端的问题，这里处理整个网络的问题）

### 发送端
- 建立套接字
- 文件切分为packets
- 将packets中的数据编码（base64编码+utf-8编码）
- 向接收端发送文件长度
- 向接收端逐个发送文件
- 关闭套接字

### 接收端
- 建立套接字
- 接收文件长度len
- 接收len个数据包packets
- 将packets中的数据解码（utf-8解码+base64解码）
- 将文件合并为file
- 关闭套接字

### TODO
- [x] 使用GBN协议/滑动窗口协议处理丢包问题和乱序问题（N=1，后续优化ing）
- [ ] 实现错误检测和纠正
- [ ] 实现流量控制机制
- [ ] 实现拥塞控制机制

![UDP文件传输 SHA-256.png](https://s2.loli.net/2023/02/12/fZxCdqWv43RLgnc.png)