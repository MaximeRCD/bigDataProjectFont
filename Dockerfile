FROM dockerproxy.repos.tech.orange/bitnami/python:3.9.15-debian-11-r12
COPY ./big_data_project ./
RUN pip install --upgrade pip 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 
# copy project

WORKDIR /app  
EXPOSE 8000


CMD ["python3", "manage.py", "makemigrations"]
CMD ["python3", "manage.py", "migrate"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
