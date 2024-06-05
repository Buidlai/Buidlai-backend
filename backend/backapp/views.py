import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer, UserStatusSerializer, PersonalInformationSerializer
from .models import UserStatus, CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

class SignUpView(APIView):
  def post(self, request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
      activation_token = str(random.randint(1000, 9999))  # Generate random 4-digit number
      user = serializer.save(is_active=False, activation_token=activation_token)
      self.send_activation_token(user.email, activation_token)
      return Response({'message': 'Account created. Check your email for activation token.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def send_activation_token(self, email, token):
    subject = 'Activation Token'
    message = f'Your activation token is: {token}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

class ActivateAccountView(APIView):
  def post(self, request):
    token = request.data.get('token')
    try:
      user = CustomUser.objects.get(activation_token=token)
    except CustomUser.DoesNotExist:
      user = None

    if user is not None and token.isdigit() and len(token) == 4:
      user.is_active = True
      user.save()
      return Response({'message': 'Account activated successfully. You can now log in.'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid activation token.'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      if user.is_active:
        # login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        serializer = CustomUserSerializer(user)
        return Response({'user': serializer.data,'token': token.key}, status=status.HTTP_200_OK)
      return Response({'message': 'Account is not activated.'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# class LogoutView(APIView):
#   def post(self, request):
#     logout(request)
#     return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class LogoutView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [TokenAuthentication]

  def post(self, request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'message': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

class UserStatusView(APIView):
  def get(self, request):
    user_statuses = UserStatus.objects.all()
    serializer = UserStatusSerializer(user_statuses, many=True)
    return Response(serializer.data)
  def post(self, request):
    serializer = UserStatusSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonalInformationView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request, user_id):
    try:
      personal_info = PersonalInformation.objects.get(user_id=user_id)
      serializer = PersonalInformationSerializer(personal_info)
      return Response(serializer.data)
    except PersonalInformation.DoesNotExist:
      return Response({'message': 'Personal information not found.'}, status=status.HTTP_404_NOT_FOUND)

  def post(self, request):
    serializer = PersonalInformationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [TokenAuthentication]

  def get(self, request):
    user = request.user
    print('user is :', user)
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)