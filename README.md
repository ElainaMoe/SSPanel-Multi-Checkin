# v2ray/SSR机场定时批量签到

自动签到使用ssPanel搭建的机场程序，支持多账户

目前此功能正在公开测试中，若有bug请到Issues反馈

支持多个机场 多个账户密码自动签到

# 使用教程

## 入门

首先，如果需要免费使用此脚本，你需要先Fork这个仓库

(如果你不会用Github，可以先问问谷歌，大概看明白了就可以一起愉快地玩耍了)

Fork之后，创建三个Secrets，名称分别是:PWD、SITE、USERS

USERS用于存放账户名称，PWD用于存放和前者对应的密码

SITE用于存放你要签到的机场的URL，需要注意格式，否则可能会出现一些BUG，这个地址例如：https://www.baidu.com 这种，带上协议，结尾不要斜杠，用回车分开

三个变量每一行都要对应上，如果是同一个站的话你需要把这个站在对应的行重复添加

保存之后就会在每天早上七点钟自动执行

# Credit

https://github.com/ifloppy/ssAutoCheckin