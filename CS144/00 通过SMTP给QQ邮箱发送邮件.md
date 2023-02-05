- [SMTP是什么？](#smtp是什么)
- [通过SMTP给QQ邮箱发送邮件](#通过smtp给qq邮箱发送邮件)
  - [1. 打开QQ邮箱的SMTP设置](#1-打开qq邮箱的smtp设置)
  - [2. 将邮箱名和获取到的授权码进行Base64编码](#2-将邮箱名和获取到的授权码进行base64编码)
  - [3. 发送邮件](#3-发送邮件)
  - [4. 具体实现](#4-具体实现)
- [收到邮件之后的样子](#收到邮件之后的样子)
- [Python程序实现流程图](#python程序实现流程图)

### SMTP是什么？

SMTP（Simple Mail Transfer Protocol）是用于在服务器之间发送电子邮件的标准协议。 它负责将电子邮件消息从一台服务器传送到另一台服务器并确保正确传送消息。 SMTP 使用一系列命令和回复在服务器之间传输电子邮件消息，它在端口 25 上运行。

### 通过SMTP给QQ邮箱发送邮件

#### 1. 打开QQ邮箱的SMTP设置

QQ邮箱网页版->邮箱设置->账户->POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务
![SMTP 1.png](https://s2.loli.net/2023/01/31/245uRUEVnT3msb6.png)

#### 2. 将邮箱名和获取到的授权码进行Base64编码

> 部分同学的邮箱名就是QQ号，直接把QQ号放进去就可以了。

[BASE64在线加密网站](https://base64.us/)

<img src="https://s2.loli.net/2023/01/31/qBKfXhpSGsgkQUy.png" height="300"></a>

#### 3. 发送邮件

**从保密的角度出发，更推荐采用SMTP专用客户端或者API发送SMTP邮件。**
这里是学习计算机网络的记录，采用telnet实现邮件发送功能。

#### 4. 具体实现

完整过程中用户输入的内容：

```C#
telnet smtp.qq.com smtp

helo qq.com

auth login

BASE64加密后的[用户名] 如SHVveXV1dQ==
BASE64加密后的[授权码] 如WXpKU2JXRnRkR2hqTW5ocllXMQ==

MAIL FROM:`<example@qq.com>`

RCPT TO:`<example@qq.com>`


DATA

Subject: Happy New Year 2023!
Dear xxx,

xxxxx, xxxxxxxx, xxxxxx, xxxxxxxx, xxxx.
xxxxxxxxx, xxxxxxxx? xxxxxx, xxxxxxx, xxx.

xxxxx, xxxxxxxx, xxxxxx, xxxxxxxx.
xxxxxxxx, xxxxxxx, xxxx.

Your xxxx,
xxxxx

.

quit
```

### 收到邮件之后的样子

<img src="https://s2.loli.net/2023/01/31/9YyE8TR2jLJ4B1I.png" ></a>

### Python程序实现流程图

![SMTP 流程图 中文.png](https://s2.loli.net/2023/02/05/DKJ2WuRz7bt658O.png)