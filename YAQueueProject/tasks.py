from __future__ import absolute_import, unicode_literals
from YAQueueProject.celery_app import app


@app.task
def add(x, y):
    return x + y
