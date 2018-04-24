from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
import bcrypt

class UserManager(models.Manager):
    def regis_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name needs to be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name needs to be at least 2 characters"
        if len(postData['password'])<8:
            errors["password"] = "Password needs to be at least 8 characters"
        if postData['password'] != postData['confirmed_psw']:
            errors["confirmed_psw"] = "Password doesn't match"
        try:
            validate_email(postData['email'])
        except:
            errors["email"] = "Email is not valid"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
