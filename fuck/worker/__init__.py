
import os

from celery import Celery

from worker import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuck.settings')

#
celery_app = Celery('fuck',broker=config.broker_url,backend=config.result_backend) # celery 名称
celery_app.conf.update(
    result_expires=config.result_expires,
)
# celery_app.config_from_object(config)# 走配置
# celery_app.autodiscover_tasks() # 自动去发现django中的任务


def call_by_worker(func):
    # celery　对任务中进行异步调用
    task = celery_app.task(func)
    return task

