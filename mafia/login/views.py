from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from .models import Choice, Question
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm


def getErrorMessages(errors_as_data):
    #return all error messages in a single list as strings.
    err_messages = []
    for val in errors_as_data.values():
        err_messages += val[0]
    return err_messages


def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            django_login(request, user)
            return redirect('/login/')
        else:
            err_messages = getErrorMessages(form.errors.as_data())
            for message in err_messages:
                messages.error(request, message)
            return render(request, 'login/index.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login/index.html', {'form': form})


def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
    return redirect('/login/')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            django_login(request, user)
            return redirect('/login/')
        else:
            err_messages = getErrorMessages(form.errors.as_data())
            for message in err_messages:
                messages.error(request, message)
            return render(request, 'login/signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'login/signup.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated.')
            #log the user in
            update_session_auth_hash(request, user)
            messages.info(request, 'You have been logged in with your new credentials.')
            return redirect('/login/')
        else:
            err_messages = getErrorMessages(form.errors.as_data())
            for message in err_messages:
                messages.error(request, message)
            return render(request, 'login/change_password.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'login/change_password.html', {'form':form})
