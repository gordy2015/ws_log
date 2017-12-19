#!/usr/bin/env python
#coding=utf-8

"""
    执行代码前需要安装
    pip install bottle,beaker
    pip install websocket-client
    pip install bottle-websocket
"""
from bottle import get, run,route, template,request,redirect,default_app,abort
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from beaker.middleware import SessionMiddleware
import time,subprocess
from ansi2html import Ansi2HTMLConverter
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#日志文件中有时会包含 ANSI 颜色高亮（如日志级别），我们可以使用 ansi2html 包来将高亮部分转换成 HTML 代码
conv = Ansi2HTMLConverter(inline=True)

#139实时查看日志
users = set()   # 连接进来的websocket客户端集合
@get('/websocket/', apply=[websocket])
def chat(ws):
    users.add(ws)
    print('add:%s'%users)
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
    print('remove:%s'%users)

#139查看历史日志最后200行
users2 = set()   # 连接进来的websocket客户端集合
@get('/websocket2/', apply=[websocket])
def chat2(ws2):
    users2.add(ws2)
    print('add2:%s'%users2)
    cmd = "/bin/tail -n 200 catalina.out"
    if users2:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        for line in popen.stdout.readlines():  # 获取内容
           for u in users2:
               line = conv.convert(line, full=False)
               u.send(line)
    users2.remove(ws2)
    print('remove2:%s'%users2)

#121实时查看日志
users3 = set()   # 连接进来的websocket客户端集合
@get('/websocket3/', apply=[websocket])
def chat3(ws3):
    users3.add(ws3)
    print('add3:%s'%users3)
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
    print('remove3:%s'%users3)

# 121SSH免密查看远程机器的历史日志最后200行
users4 = set()   # 连接进来的websocket客户端集合
@get('/websocket4/', apply=[websocket])
def chat4(ws4):
    users4.add(ws4)
    print('add4:%s'%users4)
    cmd = "/usr/bin/ssh -p 22 root@192.168.2.12 /bin/tail -n 200 /mnt/catalina.out"
    if users4:
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        for line in popen.stdout.readlines():  # 获取内容
           for u in users4:
               line = conv.convert(line, full=False)
               u.send(line)
    users4.remove(ws4)
    print('remove4:%s'%users4)


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
        return template('login.html')
    else:
        u = request.forms.get('username')
        p = request.forms.get('password')
        l = request.forms.get('login7days')
        e = request.forms.get('lenv')
        if u == 'temp' and p == '123':
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
        if not g:
            return redirect('/login')
        return func(*args, **kwargs)
    return inner

@route('/')
def index():
    abort(404)

#ws139客户端
@route('/log139')
@auth
def log139():
    return template('log139.html')

#ws121客户端
@route('/log121')
@auth
def log121():
    return template('log121.html')

dapp = default_app()
session_app = SessionMiddleware(dapp,session_opts)

run(app=session_app, host='0.0.0.0', port=8000, debug=True, reloader=True, server=GeventWebSocketServer)
