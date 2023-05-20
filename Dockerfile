#FROM dockerproxy.repos.tech.orange/python:3.9-slim-buster
FROM python:3.9-slim-buster
WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install libmariadb-dev-compat libmariadb-dev -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 

# copy project

EXPOSE 8000


CMD cd /app; python manage.py makemigrations; python manage.py migrate; python manage.py runserver 0.0.0.0:8000