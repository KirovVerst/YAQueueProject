# QProject
[![Build Status](https://travis-ci.org/KirovVerst/qproject.svg?branch=master)](https://travis-ci.org/KirovVerst/qproject)

Distributed mailing application based on Celery and RabbitMQ

## Requirements

1. Python 3.5
2. Celery 4
3. RabbitMQ 3.6
4. Docker

## Environment variables
File `variables.example.env` consists environment variable templates that are needed to run QProject application. 
1. Make sure that all of them are set in your local environment. It's required for running locally without not using docker containers.
2. Create `variables.env`. It's required for deploying using docker.
```
$ cp variables.example.env variables.env
```

## Gateway
Gateway provides REST API for clients. It is based on [Django](https://www.djangoproject.com) and [Django Rest Framework](http://www.django-rest-framework.org)). 

API documentation: `domain.example/docs/` 

### Build docker container ([on docker hub](https://hub.docker.com/r/kirovverst/gateway/)): 
```
$ docker build -t gateway -f Dockerfile.gateway .
```
### Developer mode
```
$ pip install -r requirements/dev.txt
$ python manage.py migrate
$ python manage.py runserver
```
## Worker
Worker instances provide task executions that are given by gateway instance via RabbitMQ. Worker is based on Celery.
### Build docker container ([on docker hub](https://hub.docker.com/r/kirovverst/worker/)): 
```
$ docker build -t worker -f Dockerfile.worker .
```
### Developer mode
```
$ pip install -r requirements/dev.txt
$ celery worker -A qproject -l info
```
## Deploy
Deployed application has the following services:
1. Gateway: `port 8000`
2. Worker monitoring: `port 5555`
3. Container monitoring: `port 8080`
### On one Digital Ocean droplet
```
$ cp deploy_config.example.py deploy_config.py
$ fab init deploy
```
Before deploying make sure that the size of droplet (in `deploy_config.py`) is more than 2 gb.
## Licensing

The code in this project is licensed under MIT license.
