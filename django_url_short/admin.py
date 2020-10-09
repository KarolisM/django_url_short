from django.contrib import admin
from django_url_short.models import LinkDestination


class LinkDestinationAdmin(admin.ModelAdmin):
    fields = ('user', 'link', 'destination', 'clicks')
    empty_value_display = '-empty-'
    list_filter = ('user', 'created_on')
    list_display = ('__str__', 'user', 'created_on', 'expires_on', 'expired', 'link', 'destination', 'clicks')
    search_fields = ('user', 'link', 'destination' )

admin.site.register(LinkDestination, LinkDestinationAdmin)