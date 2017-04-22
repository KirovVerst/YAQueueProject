from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('YAQueueProject',
             broker='amqp://',
             backend='rpc://',
             include=['YAQueueProject.tasks'])

if __name__ == '__main__':
    app.start()
