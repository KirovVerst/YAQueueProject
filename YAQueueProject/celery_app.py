from __future__ import unicode_literals
from celery import Celery

app = Celery('YAQueueProject')

app.config_from_object('YAQueueProject.celeryconfig')

if __name__ == '__main__':
    app.start()
