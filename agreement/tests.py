from django.test import TestCase
from django.core.urlresolvers import reverse

class agreementTest(TestCase):

    def test_URLS(self):
        response = self.client.get(reverse('agreementListURL'))
        self.assertEqual(response.status_code ,200)

