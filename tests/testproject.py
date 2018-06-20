from django.test import TestCase
from {{project_name}} import urls


class TestSett(TestCase):
    def test_project(self):
        self.assertTrue(len(urls.urlpatterns) > 0 )