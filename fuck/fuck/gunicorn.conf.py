# -*- coding: utf-8 -*-
from multiprocessing import cpu_count

bind = ["127.0.0.1:9300"] # 线上环境不会开启公网ip下，一般使用内网Ip
daemon = True #是否开启守进程
pidfile = 'logs/gunicorn.pid'

workers = cpu_count() * 2 # 工作进程数量
worker_class = "gevent" # 指定一个异步处理的库
worker_connections = 65535 # 单个进程最大连接数

keepalive = 60 # 服务器保持链接的时间，能够避免频繁的三次握手过程
timeout = 30
graceful_timeout = 10
forwarded_allow_ips = '*'

#　日志处理
capture_output = True
loglevel = 'info'
errorlog = 'logs/error.log'