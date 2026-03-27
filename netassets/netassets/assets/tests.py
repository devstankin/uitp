from django.test import TestCase, Client
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class SmokeTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_page_available(self) -> None:
        """Простейший smoke-тест: страница логина отдаёт 200."""
        # В `assets/urls.py` задан `app_name = 'assets'`, поэтому в реальных сценариях
        # URL обычно находится с неймспейсом `assets:login`.
        try:
            url = reverse("assets:login")
        except NoReverseMatch:
            # На случай, если включение URLconf настроено без неймспейса.
            url = reverse("login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

