from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20, unique=True)
    user_password = models.CharField(max_length=100)
    user_email = models.CharField(max_length=50)
    user_image = models.ImageField(upload_to='image/')
    password = None
    last_login = None
    is_superuser = None
    username = None
    first_name = None
    last_name = None
    email = None
    is_staff = None
    date_joined = None
    
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['user_email', 'user_password']

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=20, unique=True)
    team_member = models.ManyToManyField(User, related_name='team_member')

