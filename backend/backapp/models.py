from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserSatus(models.Model):
  status_name = models.CharField(max_length=100, verbose_name='User Satus', unique=True)
  description = models.TextField(max_length=500, verbose_name='User Satus Description', blank=True)

  def __str__(self):
    return self.status_name

class CustomUser(AbstractUser):
  first_name = models.CharField(max_length=200, verbose_name='Firstname')
  last_name = models.CharField(max_length=200, verbose_name='Lastname')
  username = models.
  email_address = models.
  phone_number = models.
  password = models.
  user_status = models.ForeignKey(UserStatus, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
      return self.username
