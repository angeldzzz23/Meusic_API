#!/bin/bash
python manage.py makemigrations authentication
python manage.py migrate authentication
python manage.py makemigrations api
python manage.py migrate api
python manage.py makemigrations chat
python manage.py migrate chat
python manage.py makemigrations misc
python manage.py migrate misc
python manage.py makemigrations newsfeed
python manage.py migrate newsfeed
python manage.py makemigrations preferences
python manage.py migrate preferences
python manage.py makemigrations
python manage.py migrate 
