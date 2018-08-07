#!/usr/bin/env bash
sleep 1
./manage.py makemigrations
./manage.py migrate
./manage.py initadmin
./manage.py collectstatic --no-input
./manage.py runserver 0.0.0.0:8000
