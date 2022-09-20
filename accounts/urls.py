from django.urls import path
from accounts import views

urlpatterns = [
    
    path('phone/', views.ValidatePhoneSendOTP.as_view(), name='phone'),
    path('register/', views.ValidateOTPRegister.as_view(), name='otp'),

    path('login/', views.LoginAPI.as_view(), name='login'),
]