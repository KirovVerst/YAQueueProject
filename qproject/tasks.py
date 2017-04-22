from __future__ import absolute_import, unicode_literals
from qproject.celery_app import app


@app.task
def add(x, y):
    return x + y


i = 0
j = 0


@app.task
def inc(f):
    if f % 2 == 0:
        global i
        i += 1
        return i
    else:
        global j
        j += 1
        return j
