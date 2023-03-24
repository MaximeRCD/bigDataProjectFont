FROM python:3.9-slim-buster
COPY ./big_data_project .
RUN pip install --upgrade pip 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 
RUN chmod 766 manage.py
# copy project

EXPOSE 8000



CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
