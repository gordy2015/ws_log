#!/usr/bin/env python
#coding=utf-8

"""
    执行代码前需要安装
    pip install bottle
    pip install websocket-client
    pip install bottle-websocket
"""
from bottle import get, run,route
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

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

run(host='0.0.0.0', port=8000, server=GeventWebSocketServer)
