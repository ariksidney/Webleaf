# Webleaf
A Nanoleaf Aurora WebApp

It's neither very stable nor very secure at the moment, but it kinda works.

## Guide

1. run python manage.py db init
2. python manage.py db migrate
3. python manage.py db upgrade

This should create the DB and a folder called migrations.

To start the app: python manage.py runserver
