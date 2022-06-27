# backend

## Installation

before attempting any of the commands. Make sure to create a database called musica. 

```bash
    mysql> Create DATABASE musica
```

Make sure you are in the python virtual enviroment. 

 activate virtual environment 
```bash
$ source python3-virtualenv/bin/activate
```


Modify the settings.py to fit your localhost specs
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
         'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'your username',
        'PASSWORD': 'your password',
        'NAME': 'musica',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

Run the following command to makemigrations

```bash
 python3 manage.py makemigration
```

To run Django project
```bash
  python3 manage.py runserver
```


[TODO]We dont have a requirements.txt yet, i'll make sure to add one. 
```bash
pip install -r requirements.txt
```

EndPoints

https://docs.google.com/document/d/1-Lhuk_N4GfUZFXqtigT5030osPyzw5oE7R_ehfXe8o8/edit#

