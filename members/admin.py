from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import reverse

from .models import CaretakerInvite


@admin.register(CaretakerInvite)
class CaretakerInviteAdmin(admin.ModelAdmin):
    list_display = ("email", "used", "created_at")
    readonly_fields = ("token", "used", "created_at")

    def save_model(self, request, obj, form, change):
        is_new = obj.pk is None

        super().save_model(request, obj, form, change)

        if is_new:
            invite_path = reverse(
                "members:caretaker_signup",
                kwargs={"token": obj.token},
            )

            invite_url = request.build_absolute_uri(invite_path)

            send_mail(
                subject="You're invited to join Sabay",
                message=(
                    "You've been invited to join Sabay as a caretaker.\n\n"
                    f"Create your account here:\n{invite_url}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[obj.email],
            )