# urls.py
from django.urls import path
from .views import SignUpView, ActivateAccountView, LoginView, LogoutView, UserStatusView

urlpatterns = [
  path('signup/', SignUpView.as_view(), name='signup'),
  path('activate/', ActivateAccountView.as_view(), name='activate'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('user-status/', UserStatusView.as_view(), name='user_status'),
  path('personal-info/<int:user_id>/', PersonalInformationView.as_view(), name='personal_info'),
]
