from django.urls import path,include
from django.conf import settings
from . import views


app_name = 'core'


urlpatterns = [
    path('',views.index, name="index"),
    path('settings/',views.settings, name = "settings"),
    path('signin_signup/', views.signin_signup, name = "signinSignup"),
    path('verify_otp/',views.verify_otp, name = "verify_otp"),
    path('create_post/', views.create_post, name = "create_post"),
    path('logout/', views.logout, name = "logout"),
]
