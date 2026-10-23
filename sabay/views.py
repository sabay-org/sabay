from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from booking.models import JobPost


def home(request):
    """Render the default landing page."""
    return render(request, "home.html")


""" Requiring user to be logged in """


@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    provider = getattr(request.user, "provider_profile", None)
    booking_requests = (
        JobPost.objects.select_related("seeker__user")
        .filter(status="open", provider=provider)
        .order_by("-created_at")[:5]
    )
    return render(
        request,
        "providers/dashboard.html",
        {
            "provider": provider,
            "booking_requests": booking_requests,
        },
    )
