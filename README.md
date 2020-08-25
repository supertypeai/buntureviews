## Reviews Microapp

### Project Setup Instruction

* Clone this project to your local machine
* Create your virtual environment out of this project folder by this command `python -m venv venv`
* To start virtual environment, run `source venv/bin/activate`
* Install all dependency library from requirements.txt file by this command `pip install -r requirements.txt`
* Create a DB of PostgreSQL in your local machine and update the information in `buntureviews/settings.py` file
  - The current `settings.py` file assume we have a postgres user named `devadmin`,, so unless you've update this file to specify otherwise, you may have to create it:

    ```psql
    # create user devadmin with db creation privileges
    CREATE USER devadmin WITH PASSWORD 'Ninjacoder**08' CREATEDB;

    # create database
    CREATE DATABASE buntureviews;
    ```


* For migration run `python manage.py migrate`
* To create a superuser run `python manage.py createsuperuser` and provide username, email and password

In this project several API need authentication and we are using oauth2-toolkit package. For this we have to create client_id and client_secret by following bellow procedure

* Open browser and navigate to http://localhost:8000/o/applications
* Provide a name
* client id & client secret will be generated automatically
* Select `Confidential` for `Client type`
* Select `Resource owner password-based` for `Authorization grant type`
* Save now

Created client id & client secret need to use in time of login, keep it safe. If you forget, just navigate again to this url http://localhost:8000/o/applications & you will see the name of you provided, click on it, you will get client id & client secret

## Celery Instruction
If you are new to django and celery, you can follow this link: https://realpython.com/asynchronous-tasks-with-django-and-celery/

* Install redis in your computer and run it
* In project root folder open two terminal and start virtual environment
* Run the following two command in the created terminal
  `celery -A buntureviews worker -l info`
  `celery -A buntureviews beat -l info`
