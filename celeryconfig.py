from celery import Celery

app = Celery('xufuhai', broker='mysql://root:xfh134XUFU!@localhost/celery_db', backend='mysql://root:xfh134XUFU!@localhost/celery_db')

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    result_expires=3600,
)

