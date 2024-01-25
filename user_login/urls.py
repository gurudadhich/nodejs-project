from django.contrib import admin
from django.urls import path
from user_login import views
urlpatterns = [
    path("api/v1/user/signup", views.UserSignup.as_view()),
    path("api/v1/user/login", views.UserLogin.as_view()),
]
