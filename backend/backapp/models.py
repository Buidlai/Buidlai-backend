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
  auth_token = models.CharField(max_length=4, verbose_name='Activation Token', blank=True)

  def __str__(self):
    return self.username

class PersonalInformation(models.Model):
  bio = models.TextField(max_length=500, verbose_name="User Biography")
  port_link = models.URLField(max_length=200, verbose_name="Porfolio Link")
  country = models.TextField(max_length=200, verbose_name='Country')
  language = models.TextField(max_length=200, verbose_name="Language")
  professional_role = models.TextField(max_length=200, verbose_name="Professional Role")
  resume = models.FileField(upload_to='resumes/')
  picture = models.ImageField(upload_to='pictures/')
  skills = models.TextField(max_length=500, verbose_name="Skills")
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="User", related_name='personal_information')

  def __str__(self):
    return self.user.username
