from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import resolve, reverse

from .views import home


class HomeViewTests(TestCase):
    def test_root_url_resolves_to_home_view(self):
        match = resolve("/")

        self.assertEqual(match.func, home)

    def test_home_page_renders_successfully(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "<h1>Welcome to Sabay</h1>", html=True)
        self.assertContains(response, "css/simple.min.css")

    def test_simple_css_is_available_to_staticfiles(self):
        self.assertIsNotNone(finders.find("css/simple.min.css"))
