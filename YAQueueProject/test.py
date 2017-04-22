from YAQueueProject.tasks import add

if __name__ == '__main__':
    r = add.delay(1, 1)
    print(r.get())
