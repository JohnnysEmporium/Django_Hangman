from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.log_in, name = "login"),
    path('logout', views.log_out, name = "logout"),
    path('signup', views.sign_up, name = "signup"), 
]
