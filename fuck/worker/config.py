


broker_url = 'redis://:123@127.0.0.1:6379/0'
broker_pool_limit = 100 # broker连接池，默认是０
timezone = 'Asia/Shanghai'
accept_content = ['json'] # 任务传输格式
task_serializer = 'json' # 序列化器　使用pickle -->c语言写的　比较快
enable_utc=True
result_backend = 'redis://:123@127.0.0.1:6379/0'
result_serializer = 'json'
result_cache_max = 1000 # 任务结果最大缓存量
result_expires=3600, # 任务过期时间

worker_redirect_stdouts_level = 'INFO' #日志输出