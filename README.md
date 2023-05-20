# BigDataProject

This is a Django project designed to manage and interact with quizzes in a database. It is built using Django 4.1.7. 

## Setup and Installation

To setup this project, you need to have Python and Django installed on your system. If you haven't installed them already, you can download Python from the [official website](https://www.python.org/downloads/) and then install Django using pip:

```
pip install django
```

Then, you need to clone this project to your local machine:

```
git clone https://github.com/yourusername/BigDataProject.git
```

Then navigate into the project directory:

```
cd BigDataProject
```

Install the required dependencies:

```
pip install -r requirements.txt
```

Now you should be able to run the server:

```
python manage.py runserver
```

You can access the application in your browser at `http://localhost:8000`.

## Project Structure

The main project has a number of apps each serving different functionalities:

1. `landing`: Manages the landing page of the project.
2. `dashboard`: Manages the dashboard of the project.
3. `play`: Manages the gameplay functionality.
4. `user_settings`: Manages user settings and preferences.
5. `authenticate`: Manages user authentication.
6. `custom_tags`: Contains custom template tags for the project.
7. `quiz`: Manages the quiz review functionality.

The settings of the project are contained in the `settings.py` file where you can change the database configurations, installed apps, middleware, and more.

The project is currently configured to use MySQL as its database, with a host at '34.163.143.66' and port '3306'. 

## Static Files

Static files such as CSS, JavaScript, and Images should be placed in the `static/` directory.

## Templates

The templates for each app are located in their respective directories under the `templates/` directory. 

## Custom User Model

The project uses a custom user model defined in the `authenticate` app.
