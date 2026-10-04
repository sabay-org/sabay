import secrets

from django.db import models


def generate_invite_token():
    return secrets.token_urlsafe(32)


class CaretakerInvite(models.Model):
    email = models.EmailField()
    token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_invite_token,
    )
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)