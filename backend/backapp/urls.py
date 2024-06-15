# urls.py
from django.urls import path
from .views import SignUpView, ActivateAccountView, LoginView, LogoutView, UserStatusView, CurrentUserView, PersonalInformationDetailView, PersonalInformationCreateView

urlpatterns = [
  path('signup/', SignUpView.as_view(), name='signup'),
  path('activate/', ActivateAccountView.as_view(), name='activate'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('user-status/', UserStatusView.as_view(), name='user_status'),
  path('personal-info/<int:user_id>/', PersonalInformationDetailView.as_view(), name='personal_info_detail'),
  path('personal-info/', PersonalInformationCreateView.as_view(), name='personal_info_create'),
  path('currentuser/', CurrentUserView.as_view(), name='currentuser'),
]
