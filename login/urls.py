from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('register', views.add_user, name='add_user'),
]
