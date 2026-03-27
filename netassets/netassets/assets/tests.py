from django.test import TestCase, Client
from django.urls import reverse


class SmokeTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_page_available(self) -> None:
        """Простейший smoke-тест: страница логина отдаёт 200."""
        url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

