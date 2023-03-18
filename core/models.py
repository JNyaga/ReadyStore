from django.contrib.auth.models import AbstractUser
from django.db import models


# Extending the AbstractUser model in our app to add other fields and constrants

class User(AbstractUser):
    email = models.EmailField(unique=True)
