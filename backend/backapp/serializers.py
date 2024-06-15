from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
from .models import CustomUser, UserStatus, PersonalInformation

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
  
  def create(self, validated_data):
    validated_data['password'] = make_password(validated_data['password'])
    return super().create(validated_data)

  class Meta:
    model = CustomUser
    fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'user_status', 'password']


class PersonalInformationSerializer(serializers.ModelSerializer):
  picture_url = serializers.SerializerMethodField()
  # user = CustomUserSerializer()
  username = serializers.SerializerMethodField()
  class Meta:
    model = PersonalInformation
    fields = ['id', 'bio', 'port_link', 'country', 'language', 'professional_role', 'resume', 'picture', 'skills', 'user', 'picture_url', 'username']

  def get_picture_url(self, obj):
    return obj.person_img()

  def get_username(self, obj):
    return obj.user.username

