#!/bin/bash
python3 manage.py makemigrations authentication
python3 manage.py migrate authentication
python3 manage.py makemigrations api
python3 manage.py migrate api
python3 manage.py makemigrations chat
python3 manage.py migrate chat
python3 manage.py makemigrations misc
python3 manage.py migrate misc
python3 manage.py makemigrations newsfeed
python3 manage.py migrate newsfeed
python3 manage.py makemigrations preferences
python3 manage.py migrate preferences
python3 manage.py makemigrations
python3 manage.py migrate
