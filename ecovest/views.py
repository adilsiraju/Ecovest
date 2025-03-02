from django.shortcuts import render
from django.contrib.auth import logout

def landing_page(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'landing/fullscreen.html')