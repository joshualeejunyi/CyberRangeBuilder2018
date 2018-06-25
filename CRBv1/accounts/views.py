from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
# Create your views here.

def loginsuccess(request):
    if request.user.is_staff:
        return redirect("/teachers")    
    elif request.user.is_superuser:
        return redirect("/admin")
    else:
        return redirect("/dashboard")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(email = email, username = username, password = password)
            login(request, user)
            return redirect('dashboard')

    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
