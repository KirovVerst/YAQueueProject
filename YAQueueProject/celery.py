from __future__ import absolute_import, unicode_literals
from celery import Celery

try:
    from conf import *
except:
    from conf_example import *

app = Celery('YAQueueProject',
             broker='amqp://{}:{}@{}/{}'.format(USER_NAME, PASSWORD, IP_ADDRESS, VHOST),
             backend='rpc://',
             include=['YAQueueProject.tasks'])

if __name__ == '__main__':
    app.start()
