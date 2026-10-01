from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    """Render the default landing page."""
    return render(request, "home.html")


""" Requiring user to be logged in """


@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    return render(request, "dashboard.html")
