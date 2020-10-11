from django.shortcuts import render
from django.shortcuts import redirect
from django_url_short.models import LinkDestination
from django.views.generic import View
from django_url_short.responses import CreateLinkResponse
from django_url_short.exceptions import CreateLinkError
from django_url_short.constants import HttpStatus
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.sites.shortcuts import get_current_site
from django_url_short.settings import SITE_URL, LINK_LENGTH
import random
import string
import secrets
import base64
import os


def link_redirect(request):

    link = request.get_full_path()[1:]
    if LinkDestination.objects.filter(link=link).exists():
        query = LinkDestination.objects.get(link=link)
        # TODO: check if expired, return 410
        query.clicks += 1
        query.save()
        try:
            return redirect(query.destination)
        except:
            raise Http404(f'Destination is not valid: {query.destination}')
    else:
        raise Http404(f'Link does not exist: {SITE_URL.replace("%", link)}')


class CreateLink(View):
    model = LinkDestination
    field_name = 'link'
    site = SITE_URL
    letters_and_digits = string.ascii_letters + string.digits

    def link_validation(self, destination):
        if not destination:
            raise CreateLinkError(
                status=HttpStatus.HTTP_400_BAD_REQUEST,
                msg='Empty link was submitted.',
                destination=str(destination)
            )

    def check_permissions(self, request):
        if not request.user.is_authenticated:
            raise CreateLinkError(
                status=HttpStatus.HTTP_401_NOT_AUTH,
                msg='Authentication failed! Please login.'
            )

    def create_model(self, **attrs):
        obj = self.model(
            user=self.request.user,
            **attrs
            )
        obj.save()

        return obj

    def post(self, request, *args, **kwargs):
        try:
            return self._post(request, *args, **kwargs)
        except CreateLinkError as error:
            return CreateLinkResponse(error.data, status=error.status_code)

    def get_queryset(self, destination, get_link=None):
        if get_link:
            link = get_link()
        else:
            link = self.get_link3()
        if self.model.objects.filter(link=link).exists():
            return self.get_queryset(destination)
        
        return self.create_model(link=link, destination=destination)

    def get_link1(self):
        return ''.join((random.choice(self.letters_and_digits) for i in range(LINK_LENGTH)))
    
    def get_link2(self):
        return secrets.token_urlsafe(LINK_LENGTH)[0:LINK_LENGTH]

    def get_link3(self):
        return base64.urlsafe_b64encode(os.urandom(LINK_LENGTH)).strip(b'=').decode('ascii')[0:LINK_LENGTH]

    def _post(self, request, *args, **kwargs):

        self.check_permissions(request)
        destination = request.POST.get(self.field_name)
        self.link_validation(destination)
        query = self.get_queryset(destination)

        return CreateLinkResponse(
            {
                'link': self.site.replace('%', query.link),
                'destination': query.destination,
                'expires': query.expires_on,
            },
            status=HttpStatus.HTTP_200_OK
        )