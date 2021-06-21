# TrafficMan-DB
This is the term project for the course *Database Systems Laboratory*.

## Configure Virtual Environment
Execute the following commands
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Prepare the SECRET KEY
Execute the following commands to generate secret key:
```shell
python manage.py shell
>>>from django.core.management.utils import get_random_secret_key
>>>get_random_secret_key()
'i!$!1s%4kzi%q(_^9b$i&!&apwu1!)l#=x99l2(6m=7+i(ajtm'
```

Then add the SECRET KEY to the environment variable:
```shell
export SECRET_KEY="xxxxxxxx"
```

## Prepare Database
Create a database on your MySQL server, and configure `DATABASES` at dbproject/settings.py. Please read the [document](https://docs.djangoproject.com/en/3.2/ref/databases/#mysql-notes) to 
learn more.

Run the following commands
```shell
python manage.py makemigrations TrafficMan
python manage.py migrate
```

Then run the file sql/db.sql on the database you created. You might need to change the database name *user002db* in this
file to the name of the databased you created.

## Create superuser
Create a superuser to use tha admin page
```shell
python manage.py createsuperuser
```

## Run server in debug environment
Run the following command
```shell
python manage.py runserver
```

## Deploy
Please read the [document](https://docs.djangoproject.com/en/3.2/howto/deployment/) for more information.