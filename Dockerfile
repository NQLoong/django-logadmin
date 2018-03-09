From python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt && \

cp sources.list /etc/apt/ && \

apt update && \

apt-get install expect -y && \

ssh-keygen -t rsa -P "" -f "/root/.ssh/id_rsa" 

WORKDIR /code/LogAdmin

CMD python manage.py runserver 0.0.0.0:8000 

