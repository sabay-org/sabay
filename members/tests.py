# Create your tests here.
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase 
from django.urls import reverse
from .models import Cert, Provider, Specialty, ProviderCert

User = get_user_model()

# Unit test for the Provider, Cert, Specialty, and ProviderCert models 
class ProviderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", password="password")
        self.provider = Provider.objects.create(user=self.user, city="Salem", bio="work well with dogs")

    def test_username_exists(self):
        self.assertIn("bob", str(self.provider))

    def test_bio_added(self):
        self.assertIn("work well with dogs", str(self.provider.bio))

    def test_city_added(self):
        self.assertIn("Salem", str(self.provider.city))

    def test_provider_specialties_added(self):
        cooking = Specialty.objects.create(name="Cooking")
        elderCare = Specialty.objects.create(name="Elder Care")
         
        self.provider.specialties.add(cooking, elderCare)
        names = set(self.provider.specialties.values_list("name", flat=True))
        self.assertEqual(names, {"Cooking", "Elder Care"})


class CertificateTests(TestCase):

    def setUp(self):
        self.bob = User.objects.create_user(username="bob", password="password")
        self.provider = Provider.objects.create(user=self.bob)
        self.cpr = Cert.objects.create(name="CPR")

    def  test_cert_is_linked(self):
        ProviderCert.objects.create(provider=self.provider, cert=self.cpr)
        self.assertEqual(self.provider.certifications.count(), 1)

    def test_cert_is_unique(self):
        with self.assertRaises(IntegrityError):
            Cert.objects.create(name="CPR")

    def test_multiple_providers_share_cert(self):
        john = User.objects.create_user(username="john", password="password")
        other_provider = Provider.objects.create(user=john)

        ProviderCert.objects.create(provider=self.provider , cert=self.cpr, issuer="American Red Cross")
        ProviderCert.objects.create(provider=other_provider , cert=self.cpr, issuer="American Red Cross")

        self.assertEqual(ProviderCert.objects.filter(cert=self.cpr).count(), 2)


# GET method test for autofill function
class AutofillCityTests(TestCase):
    def test_get_city_code(self):
        response = self.client.get(reverse("members:city_suggestions"), {"page": 1})
        self.assertEqual(response.status_code, 200)








