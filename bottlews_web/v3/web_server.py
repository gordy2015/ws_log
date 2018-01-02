#!/usr/bin/env python
#coding=utf-8

"""
    执行代码前需要安装
    pip install bottle,beaker
    pip install websocket-client
    pip install bottle-websocket
    pip install ansi2html
"""
from bottle import get, run,route, template,request,redirect,default_app,abort
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from beaker.middleware import SessionMiddleware
import time,subprocess
from ansi2html import Ansi2HTMLConverter
import logging
from wsconfig import WebSerconf
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#日志文件中有时会包含 ANSI 颜色高亮（如日志级别），我们可以使用 ansi2html 包来将高亮部分转换成 HTML 代码
conv = Ansi2HTMLConverter(inline=True)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='wslog.log',
                    filemode='w')

wsconfig = WebSerconf()

#139实时查看日志
users = set()   # 连接进来的websocket客户端集合
@get('/websocket/', apply=[websocket])
def chat(ws):
    users.add(ws)
    logging.debug('add:%s'%users)
    while True:
        msg = ws.receive()  # 接客户端的消息
        if msg:
            for u in users:
                # msg = conv.convert(msg, full=False)
                u.send(msg) # 发送信息给所有的客户端
        else:
            break
    # 如果有客户端断开连接，则踢出users集合
    users.remove(ws)
    logging.debug('remove:%s'%users)

#139查看历史日志最后200行
users2 = set()   # 连接进来的websocket客户端集合
@get('/websocket2/', apply=[websocket])
def chat2(ws2):
    users2.add(ws2)
    logging.debug('add2:%s'%users2)
    cmd = wsconfig.cmd2
    if users2:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        for line in popen.stdout.readlines():  # 获取内容
           for u in users2:
               line = conv.convert(line, full=False)
               u.send(line)
    users2.remove(ws2)
    logging.debug('remove2:%s'%users2)

#121实时查看日志
users3 = set()   # 连接进来的websocket客户端集合
@get('/websocket3/', apply=[websocket])
def chat3(ws3):
    users3.add(ws3)
    logging.debug('add3:%s'%users3)
    while True:
        msg = ws3.receive()  # 接客户端的消息
        if msg:
            for u in users3:
                # msg = conv.convert(msg, full=False)
                u.send(msg) # 发送信息给所有的客户端
        else:
            break
    # 如果有客户端断开连接，则踢出users集合
    users3.remove(ws3)
    logging.debug('remove3:%s'%users3)

# 121SSH免密查看远程机器的历史日志最后200行
users4 = set()   # 连接进来的websocket客户端集合
@get('/websocket4/', apply=[websocket])
def chat4(ws4):
    users4.add(ws4)
    logging.debug('add4:%s'%users4)
    cmd = wsconfig.cmd4
    if users4:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        for line in popen.stdout.readlines():  # 获取内容
           for u in users4:
               line = conv.convert(line, full=False)
               u.send(line)
    users4.remove(ws4)
    logging.debug('remove4:%s'%users4)


session_opts = {
    'session.type': 'file',
    'session.cookei_expires': 300,
    'session.data_dir': 'sessions_file',
    'session.auto': True
    }

#登陆
@route('/login',method=['GET','POST'])
def login():
    if request.method == 'GET':
        # logging.debug('request.remote_addr: %s'%request.remote_addr)
        return template('templates/login.html')
    else:
        u = request.forms.get('username')
        p = request.forms.get('password')
        l = request.forms.get('login7days')
        e = request.forms.get('lenv')
        if u == wsconfig.nuser and p == wsconfig.npwd:
            s = request.environ.get('beaker.session')
            s['user'] = u
            s['is_login'] = True
            if l:
                session_opts['session.cookei_expires'] = 604800
            # print(session_opts)
            s.save()
            if e == 'log139':
                redirect('/log139')
            else:
                redirect('/log121')
        else:
            redirect('/login')


@route('/logout',method=['GET'])
def logout():
    v = request.environ.get('beaker.session')
    # print(type(v),v) #(<class 'beaker.session.SessionObject'>, {'is_login': True, '_accessed_time': 1513199145.074627, 'user': 'temp', '_creation_time': 1513198966.570015})
    if v:
        v['is_login'] = False
    redirect('/login')

# 登陆检测装饰器
def auth(func):
    def inner(*args, **kwargs):
        v = request.environ.get('beaker.session')
        g =v.get('is_login')
        # nh = request.url.split('/')[0] + '//' + request.url.split('/')[2]
        if not g:
            redirect('/login')
        return func(*args, **kwargs)
    return inner

@route('/')
def index():
    abort(404)

#ws139客户端
@route('/log139')
@auth
def log139():
    return template('templates/log139.html')

#ws121客户端
@route('/log121')
@auth
def log121():
    return template('templates/log121.html')

dapp = default_app()
session_app = SessionMiddleware(dapp,session_opts)

run(app=session_app, host='0.0.0.0', port=26666, debug=True, server=GeventWebSocketServer)
