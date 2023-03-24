FROM bitnami/python:3.9.15-debian-11-r12
COPY ./big_data_project ./
RUN pip install --upgrade pip 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 
RUN chmod 777 manage.py
# copy project

WORKDIR /app  
EXPOSE 8000

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
