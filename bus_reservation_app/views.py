from django.shortcuts import render, redirect
from bus_reservation_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login, logout
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, "index.html")

def signin(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def auth_signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request, username=email, password=password)
        if user != None:
            login(request, user)
            if user.user_type == 1:
                return redirect('admin_home')
            else:
                return redirect("passenger_home")
        else:
            messages.error(request,"Invalid Login Details")
            return redirect("signin")

def auth_signup(request):
    pass

def user_logout(request):
    logout(request)
    return redirect('index')