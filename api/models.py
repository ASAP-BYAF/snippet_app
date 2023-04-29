from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    user_id = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
