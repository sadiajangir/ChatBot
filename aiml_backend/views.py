from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import main

session = main.ChatSession('en_core_web_sm', 'aiml_backend', 'aiml_files')
session.initiate()

def chat_aiml(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect("login_user")
    return render(request, 'aiml.html')

def user_message(request):
    message = request.POST.get('message')
    return HttpResponse(session.generate_response(message, request.user))
    