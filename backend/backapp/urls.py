from django.urls import path
from .views import SignUpView, ActivateAccountView, LoginView, LogoutView

urlpatterns = [
  path('signup/', SignUpView.as_view(), name='signup'),
  path('activate/', ActivateAccountView.as_view(), name='activate'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
]
