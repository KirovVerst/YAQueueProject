FROM python:3.5
WORKDIR /qproject
ADD . /qproject
RUN pip install -r requirements.txt
RUN python manage.py migrate
