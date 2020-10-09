from django.test import TestCase, override_settings, Client
from django_url_short.models import LinkDestination
from django.contrib.auth.forms import User


class TestCaseSet(TestCase):

    def setUp(self):
        self.user = User.objects.create(id=1259, username='testuser', email='test@test.com')
        self.user.set_password('12345')
        self.user.save()
        self.client = Client()
        logged_in = self.client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)

    def tearDown(self):
        self.user.delete()
        
    def create_entry(self, **kwargs):
        entry = LinkDestination.objects.create(
            user=self.user, 
            **kwargs,
        )
        entry.save()
        return entry