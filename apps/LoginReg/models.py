from __future__ import unicode_literals
import bcrypt
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')
# Create your models here.

class Validator(models.Manager):
    def validChecker(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name no fewer than 2 characters"
            print errors
        if len(postData['last_name']) < 2:
            errors["last_name"] = "First name no fewer than 2 characters"
            print errors
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email format"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be no fewer than 8 characters in length"
            print errors

        if (postData['password'] != postData['conf_password']):
            errors["password"] = "passwords do not match"

        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = Validator()


    # from apps.LoginRegistration.models import *
    # Users.objects.all()

#  mac$ python manage.py makemigrations
#  $ python manage.py migrate
#  python manage.py shell
# from apps.Courses.models import *
# >>> Courses.objects.all()
