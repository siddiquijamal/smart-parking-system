from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('registerationspage')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('registerationspage')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created! Please login.")
        return redirect('loginpage')

    return render(request, 'register.html')


# -------- Login --------
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('loginpage')

    return render(request, 'login.html')

# -------- Logout --------
def logout_view(request):
    logout(request)
    return redirect('loginpage')
