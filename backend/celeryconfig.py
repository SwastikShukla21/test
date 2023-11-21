from celery import Celery

app = Celery('tasks', broker='redis://127.0.0.1:6379/1',
             result_backend="redis://127.0.0.1:6379/2", enable_utc=False, timezone='Asia/Kolkata')
