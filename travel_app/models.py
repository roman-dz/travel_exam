from django.db import models
from datetime import date, time, datetime
import bcrypt
import re


# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        try:
            users = User.objects.get(email = postData['email'])
            errors['email'] = 'This email is already associated with an account.'
        except:
            pass
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match.  Please re-enter both passwords."
        
        return errors

    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match."
        return errors


class PlanManager(models.Manager):
    def travel_plan_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destination'] = "Destination name cannot be empty."
        if len(postData['description']) < 1:
            errors['description'] = "Description cannot be empty."
        if postData['date_from'] == '':
            errors['date_from'] = "Date From cannot be empty."
        if postData['date_to'] == '':
            errors['date_to'] = "Date To cannot be empty."
        else:
            ####  VALIDATE IF FUTURE DATE ####
            converted_from_date = datetime.strptime(postData['date_from'], '%Y-%m-%d')
            converted_to_date = datetime.strptime(postData['date_to'], '%Y-%m-%d')
            if converted_from_date < datetime.today():
                errors['date_from'] = "Travel Date From must be in the future."
            if converted_to_date < converted_from_date:
                errors['date_to'] = "Travel Date To should not be before Travel Date From."
            ########
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Plan(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="has_created_plans", on_delete=models.CASCADE)
    joined_by = models.ManyToManyField(User, related_name="joined_plans")
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = PlanManager()