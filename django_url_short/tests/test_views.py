from django.urls import reverse
from django_url_short.tests.utilities import TestCaseSet
from django.conf import settings
from django.test import override_settings
from django_url_short.views import CreateLink
from django_url_short.exceptions import CreateLinkError
from django_url_short.models import LinkDestination
from django.http import HttpRequest
from django_url_short.settings import LINK_LENGTH, SITE_URL


class LinkRedirectViewTests(TestCaseSet):

    @override_settings(SITE_URL='http://127.0.0.1:8000/%')
    def test_resdirect_obj_404(self):
        response = self.client.get(SITE_URL.replace('%', 'ABCDE'))
        self.assertEquals(response.status_code, 404)

    @override_settings(SITE_URL='http://127.0.0.1:8000/%')
    def test_resdirect_302(self):
        self.create_entry(destination=SITE_URL.replace('%', ''), link='ABCD')
        response = self.client.get(SITE_URL.replace('%', 'ABCD'))
        self.assertEquals(response.status_code, 302)
    
    @override_settings(SITE_URL='http://127.0.0.1:8000/%')
    def test_resdirect_404(self):
        self.create_entry(destination='blahh', link='ABCDEF')
        response = self.client.get(SITE_URL.replace('%', 'ABCDEF'))
        self.assertEquals(response.status_code, 404)


class CreateLinkPermissionsTests(TestCaseSet):
    
    @override_settings(SITE_URL='http://127.0.0.1:8000/%')
    def test_check_permissions_401(self):
        self.client.logout()
        response = self.client.post(reverse('django_url_short:api_create_link'), {'link':'blahh'})
        self.assertEquals(response.status_code, 401)


class CreateLinkTests(TestCaseSet):
    
    @override_settings(SITE_URL='http://127.0.0.1:8000/%')
    def test_validation(self):
        response = self.client.post(reverse('django_url_short:api_create_link'), {'link': ''})
        self.assertEquals(response.status_code, 400)

    @override_settings(SITE_URL='http://127.0.0.1:8000/%')
    def test_create_model_get_queryset_get_link(self):
        create_link_view = CreateLink()
        create_link_view.request = HttpRequest()
        create_link_view.request.user = self.user
        q = create_link_view.create_model(link='blahh', destination='blahh')

        self.assertEquals(q.user, self.user)
        self.assertEquals(q.link, 'blahh')
        self.assertEquals(q.destination, 'blahh')

        qs = set()
        q = create_link_view.get_queryset('blahh2')
        self.assertEquals(q.user, self.user)
        self.assertTrue(len(q.link) == LINK_LENGTH)
        self.assertIsInstance(q.link, str)
        self.assertEquals(q.destination, 'blahh2')
        qs.add(q.link)
        for _ in range(1000):
            qs.add(create_link_view.get_queryset('blahh2').link)
        self.assertEquals(len(qs), 1001)

        q = create_link_view.get_queryset('blahh4', get_link=create_link_view.get_link1)
        self.assertTrue(len(q.link) == LINK_LENGTH)
        self.assertIsInstance(q.link, str)
        self.assertEquals(q.destination, 'blahh4')

        q = create_link_view.get_queryset('blahh5', get_link=create_link_view.get_link2)
        self.assertTrue(len(q.link) == LINK_LENGTH)
        self.assertIsInstance(q.link, str)
        self.assertEquals(q.destination, 'blahh5')
        
        q = create_link_view.get_queryset('blahh6', get_link=create_link_view.get_link3)
        self.assertTrue(len(q.link) == LINK_LENGTH)
        self.assertIsInstance(q.link, str)
        self.assertEquals(q.destination, 'blahh6')

    def test_response_200(self):
        response = self.client.post(reverse('django_url_short:api_create_link'), {'link': 'blahh'})
        self.assertEquals(response.status_code, 200)

        