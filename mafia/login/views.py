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
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
# Create your views here.

class IndexView(auth_views.LoginView):
    template_name = 'login/index.html'

def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
    return redirect('/login/')

def getErrorMessages(errors_as_data):
    err_messages = []
    for val in errors_as_data.values():
        err_messages.append(val[0].message)
    return err_messages

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
            # error_data = form.errors.as_data()
            # err_messages = []
            # for val in error_data.values():
            #     err_messages.append(val[0].message)
            return render(request, 'login/signup.html', {'form': form, 'err_messages': err_messages})
    else:
        form = UserCreationForm()
        user = request.user
    return render(request, 'login/signup.html', {'form': form, 'user':user})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            #log the user in
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated.')
            return redirect('/login/')
        else:
            err_messages = getErrorMessages(form.errors.as_data())
            # error_data = form.errors.as_data()
            # err_messages = []
            # for val in error_data.values():
            #     err_messages.append(val[0].message)
            return render(request, 'login/change_password.html', {'form': form, 'err_messages': err_messages})

        # else:
        #
        #     messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'login/change_password.html', {'form':form})
