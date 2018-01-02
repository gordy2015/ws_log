#!/usr/bin/python
# encoding=utf-8
import subprocess
import time
from websocket import create_connection
from ansi2html import Ansi2HTMLConverter
from wsconfig import ClientRemote

cr = ClientRemote()

class Clog(object):
    def __init__(self):
        self.conv = Ansi2HTMLConverter(inline=True)
        self.ws = cr.ws
        self.r_log = cr.r_log
        self.r_user = cr.r_user
        self.r_ip = cr.r_ip
        self.r_port = cr.r_port
        # 配置远程服务器的IP，帐号，密码，端口等，因我做了SSH免密登陆，所以不需要密码
        self.cmd = cr.cmd
    def tailfLog(self):
        """获取远程服务器实时日志，并发送到websocket服务端"""
        popen = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        cws = create_connection(self.ws)  # 创建websocket连接
        if cws:
            while True:
                line = popen.stdout.readline().strip()  # 获取内容
                if line:
                    line = self.conv.convert(line, full=False)
                    cws.send(line)  # 把内容发送到websocket服务

if __name__ == '__main__':
    L = Clog()
    L.tailfLog()