from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    # if request.user.is_authenticated:
    #     django_logout(request)
    #     messages.info(request, 'You have been logged out.')
    # return redirect('/login/')
    return render(request, 'player_profile/index.html')
