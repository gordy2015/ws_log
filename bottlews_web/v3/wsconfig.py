#!/usr/bin/env python
#coding=utf-8

#web_server.py配置
class WebSerconf(object):
    def __init__(self):
        self.user = 'root'
        self.ip = '192.168.2.12' #远程日志文件所在的机器的IP
        self.port = '22'
        self.file = '/mnt/catalina.out'
        self.cmd4 = "/usr/bin/ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no -p {port1} {user1}@{ip1} /bin/tail -n200 {file1}".format(port1=self.port,user1=self.user,ip1=self.ip,file1=self.file)
        self.file2 = '/usr/local/nginx/html/ws_log/bottlews_web/v3/catalina.out'
        self.cmd2 = "/bin/tail -n 200 {file22}".format(file22=self.file2)
        self.nuser = 'temp'
        self.npwd = '123'


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