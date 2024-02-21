from django.urls import path,include
from django.conf import settings
from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('signin_signup/', views.signin_signup, name="signinSignup"),
    path('signin/', views.signin, name="signin"),
    path('getUser/',views.getUser,name="getUser"),
]
