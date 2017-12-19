#!/usr/bin/python
# encoding=utf-8
import subprocess
import time
from websocket import create_connection
from ansi2html import Ansi2HTMLConverter
conv = Ansi2HTMLConverter(inline=True)

class Clog(object):
    def __init__(self):
        self.r_log = 'catalina.out'
        self.ws = 'ws://192.168.2.11:8000/websocket/'
        self.cmd = "/bin/tailf {log_path}".format(log_path=self.r_log)
    def tailfLog(self):
        """获取远程服务器实时日志，并发送到websocket服务端"""
        popen = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        cws = create_connection(self.ws)  # 创建websocket连接
        if cws:
            while True:
                line = popen.stdout.readline().strip()  # 获取内容
                if line:
                    line = conv.convert(line, full=False)
                    print(line)
                    cws.send(line)  # 把内容发送到websocket服务

if __name__ == '__main__':
    L = Clog()
    L.tailfLog()