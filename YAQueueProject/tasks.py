from __future__ import absolute_import, unicode_literals
from celery_app import app


@app.task
def add(x, y):
    return x + y
