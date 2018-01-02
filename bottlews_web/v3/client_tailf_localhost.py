#!/usr/bin/python
# encoding=utf-8
import subprocess
import time
from websocket import create_connection
from ansi2html import Ansi2HTMLConverter
from wsconfig import ClientLocal


cl = ClientLocal()

class Clog(object):
    def __init__(self):
        self.conv = Ansi2HTMLConverter(inline=True)
        self.r_log = cl.r_log
        self.ws = cl.ws
        self.cmd = cl.cmd
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