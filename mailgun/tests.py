from rest_framework.test import APITestCase
from rest_framework import status


class DocsTest(APITestCase):
    def test_getting_docs(self):
        r = self.client.get('/docs/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
