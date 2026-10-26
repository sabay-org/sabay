# members/tests.py
# Create your tests here.

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


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