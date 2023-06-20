from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from py2neo import Graph

graph = Graph("bolt://localhost:7687",auth=("neo4j","12345678"))


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        authentication = list(graph.run(f"MATCH(n:USERS{{name: '{username}', password:'{password}'}}) return n.username, n.password"))[0]
        user = authenticate(username=username, password=password)
        
        print(authentication, user)
        if user is not None:
            login(request, user)
            return redirect("chat_aiml")
        else:
            print(request)
        
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect("login_user")

def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True
    return False

def add_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email= request.POST['email']
        password = request.POST['password']

        if not username_exists(username):
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            login(request, user)
            graph.run(f"MERGE(n:USERS{{name: '{username}', email: '{email}', password:'{password}'}})")

            return redirect("chat_aiml")
        else:
            print("User already exists.")
    
    return render(request, 'register.html')

