from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_url_short.settings import LINK_EXPIRATION_DELTA


class LinkDestination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, editable=True)
    destination = models.CharField(max_length=2500, null=False)
    link = models.CharField(max_length=25, unique=True, null=False)
    clicks = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.id}'

    @property
    def expires_on(self):
        return self.created_on + LINK_EXPIRATION_DELTA

    @property
    def expired(self):
        return self.expires_on <= timezone.now()