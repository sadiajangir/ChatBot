from django.shortcuts import render, redirect, HttpResponse
from . import working

# Create your views here.


def user_message(request):
    message = request.POST.get('message')
    return HttpResponse(working.response(message))

def chat(request):
    if request.user.is_anonymous:
        return redirect("login_user")
    return render(request, "chat.html")
