from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm


def sign_in(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.success(request, "Login failed. Try again")
            return redirect("core:login")
    else:
        return render(request, "core/login.html")


def sign_out(request):
    logout(request)
    return redirect("home")


def sign_up(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "core/register.html", {"form": form})

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You have singed up successfully.")
            login(request, user)
            return redirect("home")
        else:
            return render(request, "core/register.html", {"form": form})
