### SMPT是什么？

SMTP（Simple Mail Transfer Protocol）是用于在服务器之间发送电子邮件的标准协议。 它负责将电子邮件消息从一台服务器传送到另一台服务器并确保正确传送消息。 SMTP 使用一系列命令和回复在服务器之间传输电子邮件消息，它在端口 25 上运行。

### 通过SMPT给QQ邮箱发送邮件

#### 1. 打开QQ邮箱的SMPT设置

QQ邮箱网页版->邮箱设置->账户->POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务
![SMTP 1.png](https://s2.loli.net/2023/01/31/245uRUEVnT3msb6.png)

#### 2. 将邮箱名和获取到的授权码进行Base64编码

> 部分同学的邮箱名就是QQ号，直接把QQ号放进去就可以了。

![SMTP 2.png](https://s2.loli.net/2023/01/31/qBKfXhpSGsgkQUy.png)
![SMTP 3.png](https://s2.loli.net/2023/01/31/hI8HXPv9MrtCnAz.png)
[BASE64在线加密网站](https://base64.us/)

#### 3. 发送邮件

**从保密的角度出发，更推荐采用SMTP专用客户端或者API发送SMTP邮件。**
这里是学习计算机网络的记录，下面采用telnet实现邮件发送功能。

#### 4. 附录

完整过程中用户输入的内容：

```C#
telnet smtp.qq.com smtp

helo qq.com

auth login

BASE64加密后的[用户名] 如SHVveXV1dQ==
BASE64加密后的[授权码] 如WXpKU2JXRnRkR2hqTW5ocllXMQ==

MAIL FROM:"Sender Name" `<example@qq.com>`

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