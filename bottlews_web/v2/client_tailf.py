#!/usr/bin/python
# encoding=utf-8
import subprocess
import time
from websocket import create_connection
# 配置远程服务器的IP，帐号，密码，端口等，因我做了双机密钥信任，所以不需要密码
# r_user = "root"
# r_ip = "127.0.0.1"
# r_port = 22
# r_log = "/application/tomcat/logs/catalina.out"   # 远程服务器要被采集的日志路径
r_log = "catalina.out"   # 远程服务器要被采集的日志路径
# websocket服务端地址
ws_server = "ws://192.168.2.11:8000/websocket/"
# 执行的shell命令（使用ssh远程执行）
#cmd = "/usr/bin/ssh -p {port} {user}@{ip} /usr/bin/tailf {log_path}".format(user=r_user,ip=r_ip,port=r_port,log_path=r_log)
cmd = "/bin/tailf {log_path}".format(log_path=r_log)
def tailfLog():
    """获取远程服务器实时日志，并发送到websocket服务端"""
    popen = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    ws = create_connection(ws_server)   # 创建websocket连接
    if ws:
        while True:
            line = popen.stdout.readline().strip()  #获取内容
            if line:
                ws.send(line)   #把内容发送到websocket服务
if __name__ == '__main__':
    tailfLog()
