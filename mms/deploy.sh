#!/bin/sh

apt-get install virtualenv
virtualenv dj8
source  dj8/bin/activate
pip install Django==1.8.2 django_jalali django_polymorphic django-registration-redux

#python manage.py syncdb
#python ./manage.py loaddata theme/fixtures/intial_data.json


deactivate