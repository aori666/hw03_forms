from unittest import TestCase
from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        self.quest_client = Client()

    def test_homepage(self):
        response = self.quest_client.get('/')
        self.assertEqual(response.status_code, 200)