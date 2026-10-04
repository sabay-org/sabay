# members/tests.py
# Create your tests here.

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import CaretakerInvite

class SignupTests(TestCase):

    def test_signup_creates_user(self):
        response = self.client.post(
            reverse("members:signup"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "TestPassword123!",
                "confirm_password": "TestPassword123!",
            },
        )

        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertRedirects(response, reverse("members:login"))

    def test_signup_passwords_do_not_match(self):
        response = self.client.post(
            reverse("members:signup"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "TestPassword123!",
                "confirm_password": "DifferentPassword123!",
            },
        )

        self.assertFalse(User.objects.filter(username="testuser").exists())
        self.assertContains(response, "Passwords do not match")

    def test_signup_username_already_exists(self):
        User.objects.create_user(
            username="testuser",
            email="original@example.com",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("members:signup"),
            {
                "username": "testuser",
                "email": "new@example.com",
                "password": "TestPassword123!",
                "confirm_password": "TestPassword123!",
            },
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertContains(response, "Username already exists")

    def test_signup_email_already_exists(self):
        User.objects.create_user(
            username="originaluser",
            email="test@example.com",
            password="TestPassword123!",
        )

        response = self.client.post(
            reverse("members:signup"),
            {
                "username": "newuser",
                "email": "test@example.com",
                "password": "TestPassword123!",
                "confirm_password": "TestPassword123!",
            },
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertContains(response, "Email already exists")

    def test_signup_requires_all_fields(self):
        response = self.client.post(
            reverse("members:signup"),
            {
                "username": "",
                "email": "",
                "password": "",
                "confirm_password": "",
            },
        )

        self.assertFalse(User.objects.exists())
        self.assertContains(response, "All fields are required")
class CaretakerInviteTests(TestCase):

    def setUp(self):
        self.invite = CaretakerInvite.objects.create(
            email="caretaker@example.com"
        )

        self.invite_url = reverse(
            "members:caretaker_signup",
            args=[self.invite.token],
        )

    def test_valid_invite_displays_signup_page(self):
        response = self.client.get(self.invite_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "caretaker@example.com")

    def test_invalid_invite_displays_invalid_page(self):
        response = self.client.get(
            reverse(
                "members:caretaker_signup",
                args=["fake-token"],
            )
        )

        self.assertContains(response, "Invalid Invitation")

    def test_caretaker_signup_creates_user(self):
        response = self.client.post(
            self.invite_url,
            {
                "username": "caretaker1",
                "password": "TestPassword123!",
                "confirm_password": "TestPassword123!",
            },
        )

        self.assertTrue(
            User.objects.filter(
                username="caretaker1",
                email="caretaker@example.com",
            ).exists()
        )

        self.assertRedirects(response, reverse("members:login"))

    def test_caretaker_signup_marks_invite_used(self):
        self.client.post(
            self.invite_url,
            {
                "username": "caretaker1",
                "password": "TestPassword123!",
                "confirm_password": "TestPassword123!",
            },
        )

        self.invite.refresh_from_db()

        self.assertTrue(self.invite.used)

    def test_used_invite_cannot_be_reused(self):
        self.invite.used = True
        self.invite.save()

        response = self.client.get(self.invite_url)

        self.assertContains(response, "Invalid Invitation")
@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
)
class CaretakerInviteAdminTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="TestPassword123!",
        )

        self.client.force_login(self.admin)

    def test_admin_creating_invite_sends_email(self):
        response = self.client.post(
            reverse("admin:members_caretakerinvite_add"),
            {
                "email": "newcaretaker@example.com",
                "_save": "Save",
            },
        )

        self.assertEqual(response.status_code, 302)

        invite = CaretakerInvite.objects.get(
            email="newcaretaker@example.com"
        )

        self.assertFalse(invite.used)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to,
            ["newcaretaker@example.com"],
        )

        invite_url = reverse(
            "members:caretaker_signup",
            args=[invite.token],
        )

        self.assertIn(invite_url, mail.outbox[0].body)