from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=90)
    curp = models.CharField(max_length=18, null=True)
    cp = models.CharField(max_length=5, null=True)
    rfc = models.CharField(max_length=13, null=True)
    telephone = models.CharField(max_length=10, null=True)
    date = models.DateField(null=True)
    address = models.CharField(max_length=200)