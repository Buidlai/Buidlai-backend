from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer

User = get_user_model()

class SignUpView(APIView):
  def post(self, request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save(is_active=False)

      uid = urlsafe_base64_encode(force_bytes(user.pk))
      token = default_token_generator.make_token(user)
      self.send_activation_token(user.email, uid, token)

      return Response({'message': 'Account created. Check your email for activation token.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def send_activation_token(self, email, uid, token):
    subject = 'Activation Token'
    message = f'Your activation token is: {token}\nUse this UID: {uid}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

class ActivateAccountView(APIView):
    def post(self, request):
        uidb64 = request.data.get('uidb64')
        token = request.data.get('token')
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully. You can now log in.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid activation token or UID.'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'message': 'Account is not activated.'}, status=status.HTTP_403_FORBIDDEN)
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
  def post(self, request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
