FROM bitnami/python:3.9.15-debian-11-r12

WORKDIR /usr/src/app/big_data_project

RUN pip install --upgrade pip 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 
# copy project
COPY . /usr/src/app

EXPOSE 8000


CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
