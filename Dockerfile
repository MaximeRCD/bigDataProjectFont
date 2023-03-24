FROM python:3.9-slim-buster
COPY ./big_data_project ./
RUN pip install --upgrade pip 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 

# copy project

EXPOSE 8000
WORKDIR /app
CMD ["python", "manage.py", "makemigrations"]
WORKDIR /app
CMD ["python", "manage.py", "migrate"]
WORKDIR /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
