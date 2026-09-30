from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

"""
Decided to use a custom login view
- makes sure the request method is post before authenticating
- checks to make sure user exists before calling auth
"""


def login(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            error = "Invalid username or password"

    return render(request, "auth_logic/login.html", {"error": error})


"""
Using a very simple logout view atm. 
- makes sure the request method is post
"""


@require_POST
def logout(request):
    auth_logout(request)
    return redirect("home")
