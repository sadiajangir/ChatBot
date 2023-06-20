from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('aiml', views.chat_aiml, name='chat_aiml'),
    path('aiml/user_message/', views.user_message, name="user_message"),
]