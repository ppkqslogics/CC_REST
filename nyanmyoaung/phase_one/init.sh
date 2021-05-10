#!/bin/bash
#set -e

#echo "Starting SSH ..."
#service ssh start
#systemctl start ssh

python /code/manage.py makemigrations
python /code/manage.py migrate
# python /code/manage.py runserver 0.0.0.0:8000
gunicorn user.wsgi:application --bind 0.0.0.0:8000
