from rest_framework import serializers
from .models import CustomUser, UserStatus
from django.contrib.auth import password_validation


class UserStatusSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserStatus
    fields = ['id', 'status_name', 'description']

class CustomUserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
    write_only=True,
    required=True,
    style={'input_type': 'password'}
  )

  def validate_password(self, value):
    password_validation.validate_password(value)
    return value

  class Meta:
    model = CustomUser
    fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'user_status', 'password']
