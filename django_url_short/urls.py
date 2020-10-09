from django.urls import path
from django_url_short import views
from django.conf.urls import url

app_name = 'django_url_short'
urlpatterns = [
    path('api/create_link', views.CreateLink.as_view(), name='api_create_link'),
    url(r'^.+', views.link_redirect, name='link_redirect'),
]
