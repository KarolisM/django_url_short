from django.http import HttpResponse
from django_url_short.settings import ENCODER, CONTENT_TYPE


class CreateLinkResponse(HttpResponse):
    """
    Inherits HttpResponse object and overrides init method.

    Args:
        content (dict): contents data to be returned.
        status (int): Http status code.
        *args: additional arguments.
        **kwargs: additional keyword arguments.

    Returns:
        HttpResponse: HttpResponse
    """

    def __init__(self, content, status=None, *args, **kwargs):
        super(CreateLinkResponse, self).__init__(
            content=ENCODER(content),
            content_type=CONTENT_TYPE,
            status=status,
            *args, **kwargs
        )