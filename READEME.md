## Reviews Microapp

### Project Setup Instruction

* Clone this project to your local machine
* Create your virtual environment out of this project folder by this command `python -m venv venv`
* To start virtual environment, run `source venv/bin/activate`
* Install all dependency library from requirements.txt file by this command `pip install -r requirements.txt`
* Create a DB of PostgreSQL in your local machine and update the information in `buntureviews/settings.py` file
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

* Login API:    `http://localhost:8000/o/token/`
  data format:
  ```
  {
    "grant_type": "password",
    "client_id": "ZmhHa7x3doe30HToe9merNOPDo2EmEdyz88T3b2d",
    "client_secret": "qtnrfKTYM9iS6Vh18W8vedN9kvzuKPHT0SqKVEIDbSCRbg1wCcgauCYyO4Bk8WRKalvjjYpft2XsEVc4EfsqnsYNdBCaPc1hQKrrCJMYi4qlXaTV4jlooupfEA0WBIy6",
    "username": "devadmin",
    "password": "Ninjacoder**08"
  }
  ```
  Here you have to change the client_id & the client_secret, username & the password of user who will be logged in.