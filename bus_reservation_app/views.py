from django.shortcuts import render, redirect
from bus_reservation_app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib import messages
from .models import CustomUser

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
                return redirect("student_home")
        else:
            messages.error(request,"Invalid Login Details")
            return redirect("signin")

def auth_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        address = request.POST.get('address')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email, user_type=2)
            user.student.phone_number = phone_number
            user.student.address = address
            user.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}")
            return redirect("student_home")
        
        except Exception as e:
            print(e)
            messages.error(request, "An Error occured, please try again")
            return redirect("signup")
    else:
        return HttpResponse("Method Not Allowed")

def user_logout(request):
    logout(request)
    return redirect('index')