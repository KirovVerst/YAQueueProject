from __future__ import absolute_import, unicode_literals
from YAQueueProject.tasks import add

if __name__ == '__main__':
    for i in range(10):
        r = add.apply_async((i, i))
        print(r.get())
