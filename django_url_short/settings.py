from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import datetime
import os

DEFAULT_SITE_URL = 'http://127.0.0.1:8000/%'
SITE_URL = getattr(settings, 'SITE_URL', DEFAULT_SITE_URL)
DEFAULT_ENCODER = DjangoJSONEncoder().encode
ENCODER = getattr(settings, 'ENCODER', DEFAULT_ENCODER)
DEFAULT_CONTENT_TYPE = 'application/json'
CONTENT_TYPE = getattr(settings, 'CONTENT_TYPE', DEFAULT_CONTENT_TYPE)
DEFAULT_LINK_EXPIRATION_DELTA = datetime.timedelta(days=1)
LINK_EXPIRATION_DELTA = getattr(settings, 'LINK_EXPIRATION_DELTA', DEFAULT_LINK_EXPIRATION_DELTA)
DEFAULT_LINK_LENGTH = 8
LINK_LENGTH = getattr(settings, 'LINK_LENGTH', DEFAULT_LINK_LENGTH)