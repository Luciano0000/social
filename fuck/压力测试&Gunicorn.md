# 测试
## 功能测试
## 压力测试
- 测试服务器的性能
### 常用工具
- ab(apache benchmark)
    - Ubuntu下安装ab:``apt-get install apache2-utils``
    - 压力测试：``ab -n 请求数 -c 用户量 http://127.0.0.1:8000/``
- siege
- webbench
- wrk
#### echo测试：整个系统最大性能(使用gevent,在linux下能够达到 8000r/s　左右)
#### 带缓存测试: 3000r/s ~ 5000r`/s
#### 带数据库测试: 300r/s
# gunicorn
### 切记：启动gunicorn之后在启动Django的WSGI服务器
- gunicorn库:``pip install gunicorn``
- 协程库:``pip install gevent``
- 开启gunicorn:``gunicorn -c 文件.py 工程名.wsgi``
- ``gunicorn -c fuck/gunicorn-config.py fuck.wsgi``
#### Gunicorn 进程模型
- master : 主进程(只负责管理子进程，自身不接受用户请求)
- worker : 工作进程(fork 主进程而来的，接受处理所有的用户请求)
#### 查看gunicorn的进程状态``ps aux|grep gunicorn``
#### 查看端口号为9000的网络状态信息:``netstat -nat|grep 9000``
```python
luciano@luciano:~/Desktops/fuck$ netstat -nat|grep 9000
tcp        0      0 127.0.0.1:9000          0.0.0.0:*               LISTEN   
```
#### KeepAlive:让ＴCP保持一定的连接时间

