FROM ubuntu:16.04
WORKDIR /home/user/worker
COPY . /home/user/worker
RUN apt update
RUN apt install -y python python-dev python-distribute python-pip
RUN pip install -r requirements.txt
CMD ["celery", "worker", "-A", "qproject", "-l", "info"]