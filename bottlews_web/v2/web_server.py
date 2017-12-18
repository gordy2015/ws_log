#!/usr/bin/env python
#coding=utf-8

"""
    执行代码前需要安装
    pip install bottle
    pip install websocket-client
    pip install bottle-websocket
"""
from bottle import get, run,route, template,request,redirect,default_app
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
from beaker.middleware import SessionMiddleware

#实时查看日志
users = set()   # 连接进来的websocket客户端集合
@get('/websocket/', apply=[websocket])
def chat(ws):
    users.add(ws)
    print('add:%s'%users)
    while True:
        msg = ws.receive()  # 接客户端的消息
        if msg:
            print(msg)
            for u in users:
                u.send(msg) # 发送信息给所有的客户端
        else:
            print('Not any msg')
            break
    # 如果有客户端断开连接，则踢出users集合
    users.remove(ws)
    print('remove:%s'%users)

#查看历史日志
users2 = set()   # 连接进来的websocket客户端集合
@get('/websocket2/', apply=[websocket])
def chat2(ws2):
    users2.add(ws2)
    print('add2:%s'%users2)
    if users2:
        with open('test.log','r') as f:
            for line in f.readlines():
                msg = line
                for u in users2:
                    u.send(msg)
    users2.remove(ws2)
    print('remove2:%s'%users2)

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
        if u == 'temp' and p == '123':
            s = request.environ.get('beaker.session')
            s['user'] = u
            s['is_login'] = True
            if l:
                session_opts['session.cookei_expires'] = 604800
            print(session_opts)
            s.save()
            redirect('/log139')
        else:
            redirect('/login')

# 登陆检测装饰器
def auth(func):
    def inner(*args, **kwargs):
        v = request.environ.get('beaker.session')
        g =v.get('is_login')
        print(v,g)
        if not g:
            return redirect('/login')
        return func(*args, **kwargs)
    return inner

@route('/')
def index():
    return '404 NOT FOUND'

#ws客户端
@route('/log139')
@auth
def log139():
    return template('log139.html')

dapp = default_app()
session_app = SessionMiddleware(dapp,session_opts)

run(app=session_app, host='0.0.0.0', port=8000, debug=True, reloader=True, server=GeventWebSocketServer)
