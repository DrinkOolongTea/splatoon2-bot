<p align="center">
  <img align="center" src="https://v2.nonebot.dev/logo.png"><br>

  <a href="https://github.com/DrinkOolongTea/splatoon2-bot/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-GPL-informational">
  </a>
  
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.2-green">
  </a>
  
  <a href="">
    <img src="https://img.shields.io/badge/release-v1.3.1-orange">
  </a>
  
</p>

<div align="center">

# Splatoon2 Bot

</div>

## 使用说明
依赖于nonebot2，nonebot2相关信息可以参考官网：https://v2.nonebot.dev/
### 安装方法
安装命令
```
nb plugin install nanobot-plugin-splatoon2tools
```
在nonebot2代码根目录bot.py中写入，具体位置可以参考：https://v2.nonebot.dev/docs/tutorial/plugin/load-plugin
```
nonebot.load_plugin("splatoon2_tools")
```
启动bot.py即可
### 命令使用说明
私聊或者群聊发送
```
/工
/凃地
/单排
/组排
/推送
```
超级管理员命令
```
/开启自动推送
/关闭自动推送
```
超级管理员手动更新数据
```
/更新
```
可在喷2每次更新后自动推送

### 配置文件说明
配置文件在bot.py目录的.env,加入以下内容
```
# 超级用户列表
SUPERUSERS = ["xxxxx"]
# 代理地址 没有可以不填
HTTPS_PROXY = "123.123.123.123"
# 代理端口 没有可以不填
PROXY_PORT = 1234
# 定时推送的群号列表
GROUP_ID_LIST = ["xxxxx"]
# bot的qq
BOT_QQ = "xxxxx"
# bot群转发的昵称
BOT_QQ_NAME = "xxxxx"

```

## 插件更新日志

### v1.3.1 更新内容
* 修复v1.3.0版本bug
* 更改字体，更贴合喷喷设定
* 增加命令 `推送` 可一次性推送全部内容
* 增加缓存功能可靠性
* 修复打工结束时间如果为00:00不会跳转到下一天的bug

### v1.3.0（2.0前瞻） 更新内容（废弃）
* 增加代理功能，增加自动推送功能，优化代码逻辑，优化处理逻辑，增加缓存功能，同时修改获取数据为并发，减少阻断时间
* 感谢[Sichongzou](https://github.com/Sichongzou)提供的灵感以及代码示范[示范地址](https://github.com/Sichongzou/splatoon2-bot)。

* 2.0.0预览 追加可用命令新加自动推送群组，增加群主和管理员管理机制，追加喷三倒计时…………

### v1.2.4 更新内容（废弃）
* 增加代理功能可在bot程序根目录加入配置文件 `splatoon2_tools_config.ini` 文件内容如下文所示,留空或者没有该配置文件为无代理
```
[proxy]
https_proxy = xxx.xxx.xxx.xxx
port = xx
```
不知道根目录在哪的可在nonebot启动程序内执行下面代码获取(一般为bot.py所在目录)
```
print(os.getcwd())
```
### v1.1.1 更新内容
* 处理字体资源无法打开问题
### v1.1.0 更新内容
* 凃地、单排、组排查询添加时间显示
### v1.0.4 更新内容
* 发布至pypi，发布至nonebot2商店
### v1.0.0 更新内容
* 增加“/凃地，/单排，/组排”命令，优化代码
### v0.1.2 更新内容
* 美化回复构图，优化代码
### v0.1 更新内容
* 实现 “/工” 查询当日打工内容

## 插件声明
### tips
* 要注意部署所在服务器的时区，要不然就会出现发送的图片时间不对的情况
```
docker部署可以在dockerfile里加上
ENV TZ=Asia/Shanghai

或者docker run的时候加上
-e TZ="Asia/Shanghai"
```

### 数据来源
* splatoon-wiki：https://splatoonwiki.org/

### 其他
* 今天才发现插件前缀错了，应该为nonebot，自己不小心写成了nanobot，而且一直没有注意到，这里也不打算改了，一个原因是不打算麻烦官方了
另外一个也算是对自己的一个要仔细检查的提醒吧。