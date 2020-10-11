from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django_url_short.models import LinkDestination


class ExpiredFilter(SimpleListFilter):
    title = 'expired links'
    parameter_name = 'expired'

    def lookups(self, request, model_admin):
        return (('expired', 'expired'),)

    def queryset(self, request, queryset):
        if self.value() == 'expired':
           filtered = (x.id for x in queryset if x.expired)
           return queryset.filter(id__in=filtered)
        
        return queryset


class LinkDestinationAdmin(admin.ModelAdmin):
    fields = ('user', 'link', 'destination', 'clicks')
    empty_value_display = '-empty-'
    list_filter = ('user', 'created_on', ExpiredFilter,)
    list_display = ('__str__', 'user', 'created_on', 'expires_on', 'expired', 'link', 'destination', 'clicks')
    search_fields = ('user__username', 'link', 'destination')


admin.site.register(LinkDestination, LinkDestinationAdmin)