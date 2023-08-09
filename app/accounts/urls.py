from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static

urlpatterns = [
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('', views.dashboard, name='dashboard'),
  path('activate/<uidb64>/<token>', views.activate, name='activate'),
  path('otp/', views.check_otp, name='check_otp'),
  path('otp_generation/', views.otp_generation, name='otp_generation'),
  path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
  path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name='resetpassword_validate'),
  path('profile', views.user_profile, name='profile'),
  path('user_activaation_mail/<str:email>', views.user_activaation_mail_send, name='user_activaation_mail')
] 


