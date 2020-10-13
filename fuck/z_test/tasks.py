from celery import Celery

app = Celery('tasks', broker='redis://:123@127.0.0.1:6379/0',result_expires=3600)

def call_by_worker(func):
    # celery　对任务中进行异步调用
    task = app.task(func)
    return task

@call_by_worker
def add(x, y):
    return (x + y)

if __name__ == '__main__':
    a = add(1,2)
    print(a)