from django.shortcuts import render
from django.contrib.auth.decorators import login_required
""" Importing global var """ 
from django.conf import settings

def home(request):
    """Render the default landing page."""
    return render(request, 'home.html')

""" Requiring user to be logged in """
@login_required(login_url= settings.LOGIN_URL)
def dashboard(request):
    if request.user.is_authenticated:
       return render(request, 'dashboard.html')
    else:
       return LoginPage(request)

