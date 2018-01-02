#!/usr/bin/env python
#coding=utf-8
#为日志文件生成测试数据（仅供测试）
import time
import random
log_path = 'catalina.out'
while 1:
    with open(log_path,'a') as f:
        f.write('\033[31m[%s] %s\033[0m \n' % (time.ctime(),random.random()))
    time.sleep(2)
