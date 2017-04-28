# QProject
[![Build Status](https://travis-ci.org/KirovVerst/qproject.svg?branch=master)](https://travis-ci.org/KirovVerst/qproject)

Distributed application based on Celery and RabbitMQ

## Requirements

1. Python 3.5
2. Celery 4
3. RabbitMQ 3.6

## Gateway
Gateway provides REST API for clients. It is based on [Django](https://www.djangoproject.com) and [Django Rest Framework](http://www.django-rest-framework.org)).
You can build gateway container: 
```
$ docker build -t worker -f Dockerfile.worker .
```
Link to ready docker container: https://hub.docker.com/r/kirovverst/gateway/
```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```

## Licensing

The code in this project is licensed under MIT license.
