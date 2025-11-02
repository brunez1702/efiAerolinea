from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')

def reservar(request):
    return render(request, 'reservar.html')

def crear_cuenta(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese nombre de usuario ya existe.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, "Cuenta creada exitosamente.")
            return redirect('home')

    return render(request, 'crear_cuenta.html')
