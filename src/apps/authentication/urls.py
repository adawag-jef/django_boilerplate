from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    RequestPasswordResetEmail,
    PasswordTokenCheckAPIView,
    SetNewPasswordAPIView,
    ArchiveUserView
)
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('archive/<code>/', ArchiveUserView.as_view(), name='archive'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-password/', RequestPasswordResetEmail.as_view(),
         name='request_reset_password'),
    path('password-reset/<uidb64>/<token>',
         PasswordTokenCheckAPIView.as_view(), name='password_reset_confirm'),
    path('reset-password/', SetNewPasswordAPIView.as_view(),
         name='reset_password')

]
