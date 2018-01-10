#!/usr/bin/env python
#coding=utf-8
import os, subprocess
#web_server.py配置
class WebSerconf(object):
    def __init__(self):
        self.user = 'root'
        self.ip = '192.168.2.12' #远程日志文件所在的机器的IP
        self.port = '22'
        self.file = '/mnt/catalina.out'
        self.cmd4 = "/usr/bin/ssh -oStrictHostKeyChecking=no -p {port1} {user1}@{ip1} /bin/tail -n300 {file1}".format(port1=self.port,user1=self.user,ip1=self.ip,file1=self.file)
        self.file2 = '/usr/local/nginx/html/ws_log/bottlews_web/v3/catalina.out'
        self.mt = '/bin/tail -n 300'
        self.cmd2 = "{mt} {file22}".format(mt=self.mt,file22=self.file2)
        self.nuser = 'temp'
        self.npwd = '123'
    def gcmd139(self):
        mcmd = "ls msgj_log/gateway-201*|awk -F '[-.]' '{print $2$3$4}'"
        mf = 'ls msgj_log/'
        mt = '/bin/tail -n 300'
        c = os.popen(mcmd)
        a = []
        for i in c.readlines():
            w = int(i.strip())
            a.append(w)
        a.reverse()
        b = str(a[0])
        q = 'gateway-' + b[0:4] + '-' + b[4:6] + '-' + b[6:8] + '*'
        mfind = "%s%s" %(mf,q)
        # print(a[0])
        if len(b) == 8:
            r = subprocess.Popen(mfind, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            file = r.stdout.readline().strip()
            cmd = "%s %s"%(mt,file)
            return file,cmd

    def gcmd121(self):
        md = "ls /tmp/testtt/gateway-201*|awk -F '[-.]' '{print $2$3$4}'"
        mcmd = "/usr/bin/ssh -oStrictHostKeyChecking=no -p {port1} {user1}@{ip1} {md}".format(port1=self.port,user1=self.user,ip1=self.ip,md=md)
        mf = '/usr/bin/ssh -oStrictHostKeyChecking=no -p {port1} {user1}@{ip1} ls /tmp/testtt/'.format(port1=self.port,user1=self.user,ip1=self.ip)

        c = os.popen(mcmd)
        a = []
        for i in c.readlines():
            w = int(i.strip())
            a.append(w)
        a.reverse()
        b = str(a[0])
        q = 'gateway-' + b[0:4] + '-' + b[4:6] + '-' + b[6:8] + '*'
        mfind = "%s%s" % (mf, q)
        # print(a[0])
        if len(b) == 8:
            r = subprocess.Popen(mfind, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            file = r.stdout.readline().strip()
            cmd = "/usr/bin/ssh -oStrictHostKeyChecking=no -p {port1} {user1}@{ip1} {mt} {file}".format(port1=self.port,user1=self.user,ip1=self.ip,mt=self.mt,file=file)
            return file, cmd

#client_tailf_localhost.py配置
class ClientLocal(object):
    def __init__(self):
        self.r_log = 'catalina.out'
        self.ws = 'ws://192.168.2.11:26666/websocket/'
        self.cmd = "/bin/tailf {log_path}".format(log_path=self.r_log)


#client_tailf_remote.py配置
class ClientRemote(object):
    def __init__(self):
        self.ws = 'ws://192.168.2.11:26666/websocket3/'
        self.r_log = '/mnt/catalina.out'
        self.r_user = "root"
        self.r_ip = "192.168.2.12"  #远程日志文件所在的机器的IP
        self.r_port = 22
        # 配置远程服务器的IP，帐号，密码，端口等，因我做了SSH免密登陆，所以不需要密码
        self.cmd = "/usr/bin/ssh -p {port} {user}@{ip} /usr/bin/tailf {log_path}".format(user=self.r_user, ip=self.r_ip,
                                                                                         port=self.r_port,
                                                                                         log_path=self.r_log)


#client_tailf_remote_ms.py配置
class ClientRemoteMs(object):
    def __init__(self):
        self.ws = 'ws://192.168.2.11:26666/websocket6/'
        self.r_log = WebSerconf().gcmd121()[0]
        self.r_user = "root"
        self.r_ip = "192.168.2.12"  #远程日志文件所在的机器的IP
        self.r_port = 22
        # 配置远程服务器的IP，帐号，密码，端口等，因我做了SSH免密登陆，所以不需要密码
        self.cmd = "/usr/bin/ssh -p {port} {user}@{ip} /usr/bin/tailf {log_path}".format(user=self.r_user, ip=self.r_ip,
                                                                                         port=self.r_port,
                                                                                         log_path=self.r_log)