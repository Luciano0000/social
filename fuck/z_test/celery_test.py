# 安装：pip install 'celery[redis]'

#　创建实例
import time
from celery import Celery

broker = 'redis://127.0.0.1:6379'
backend = 'redis://127.0.0.1:6379/0'
app  = Celery('my_tesk',broker=broker,backend=backend)
@app.task
def add(x,y):
    time.sleep(5)
    return x+y


# 启动Worker
##```celery worker -A task --loglevel=info```


# 调用任务
# from celery_test import add
add.dalay(2,8)

# 常规配置
broker_url = 'redis://127.0.0.1:6379/0'
broker_pool_limit = 1000 # broker连接池，默认是０
timezone = 'Asia/Shanghai'
accept_content = ['pickle','json']
task_serializer = 'pickle'
result_expires = 3600 # 任务过期时间
result_backend = 'redis://127.0.0.1:6379/0'
result_serializer = 'pickle'
result_cache_max = 10000 # 任务结果最大缓存量
worker_redirect_stdouts_level = 'INFO'