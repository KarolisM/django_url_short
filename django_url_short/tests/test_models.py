from django_url_short.models import LinkDestination
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.db import IntegrityError, transaction
from django.test.signals import setting_changed
from django_url_short.tests.utilities import TestCaseSet
from django_url_short.settings import LINK_EXPIRATION_DELTA
import django_url_short


class LinkDestinationTest(TestCaseSet):

    def test_str(self):
        entry = self.create_entry(
            destination='testdestination', 
            link='testlink'
        )
        self.assertIsInstance(entry, LinkDestination)
        self.assertEqual(str(entry), str(entry.id))

    def test_date(self):
        entry = self.create_entry(
            destination='testdestination2', 
            link='testlink2'
        )
        self.assertTrue((timezone.now() - entry.created_on) < timedelta(minutes=1) )
        self.assertEqual((entry.expires_on - entry.created_on), LINK_EXPIRATION_DELTA)

    def test_expired(self):
        entry = self.create_entry(
            destination='testdestination3', 
            link='testlink3'
        )
        # a hack to everride LINK_EXPIRATION_DELTA, since it is imported from apps settings.
        entry.created_on -= LINK_EXPIRATION_DELTA
        entry.save()
        self.assertTrue(entry.expired)

    @transaction.atomic
    def test_IntegrityError_link(self):
        self.create_entry(
            destination='testdestination4', 
            link='testlink4'
        )
        with self.assertRaises(IntegrityError):
            self.create_entry(
                destination='testdestination4', 
                link='testlink4'
            )
