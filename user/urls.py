from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),
     path('chat', views.chat, name='chat'),
    path('user_message/', views.user_message, name="user_message"),
]