from django.shortcuts import render, HttpResponseRedirect
from users.forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth
from django.urls import reverse


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('employees_list'))
    else:
        form = UserLoginForm()
    context = {'form': UserLoginForm()}
    return render(request, 'login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))
