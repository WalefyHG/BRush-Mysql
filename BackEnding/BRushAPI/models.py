from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20, unique=True)
    user_password = models.CharField(max_length=100)
    user_email = models.CharField(max_length=50)
    user_image = models.ImageField(upload_to='image/', null=True, blank=True)
    user_birthday = models.DateField(null=True, blank=True)
    user_firstName = models.CharField(max_length=50)
    user_lastName = models.CharField(max_length=50)
    is_confirmed = models.BooleanField(default=False)
    user_idioma = models.CharField(max_length=20)
    user_games = models.CharField(max_length=50)
    user_pais = models.CharField(max_length=20)
    user_banner = models.ImageField(upload_to='banner/', null=True, blank=True)
    user_youtube = models.CharField(max_length=100, null=True, blank=True)
    user_twitch = models.CharField(max_length=100, null=True, blank=True)
    user_instagram = models.CharField(max_length=100, null=True, blank=True)
    user_twitter = models.CharField(max_length=100, null=True, blank=True)
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

class Notices(models.Model):
    notice_id = models.AutoField(primary_key=True)
    notice_title = models.CharField(max_length=100)
    notice_content = models.TextField()
    notice_date = models.DateTimeField(auto_now_add=True)
    notice_image = models.ImageField(upload_to='newsImage/', null=True, blank=True)
    notice_writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notice_writer')
    
class UserCode(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, unique=True)
    verification_code_expires = models.DateTimeField(null=True)