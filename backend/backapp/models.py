from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserStatus(models.Model):
  status_name = models.CharField(max_length=100, verbose_name='User Status', unique=True)
  description = models.TextField(max_length=500, verbose_name='User Status Description', blank=True)

  def __str__(self):
      return self.status_name

class CustomUser(AbstractUser):
  phone_number = models.CharField(max_length=15, verbose_name='Phone Number', blank=True, null=True)  # Optional phone number field
  user_status = models.ForeignKey(UserStatus, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='User Status')

  def __str__(self):
    return self.username
