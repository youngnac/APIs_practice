from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class MyUser(AbstractUser):
    def __str__(self):
        return '{}{}'.format(
            self.last_name,
            self.first_name,
        )
