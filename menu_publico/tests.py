from django.test import TestCase
from django.urls import reverse

class MenuPublicoViewTests(TestCase):
    def test_menu_index_view_status_code_and_template(self):
        url = reverse('menu_publico:menu_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu_publico/index.html')
        self.assertIn('platos', response.context)
