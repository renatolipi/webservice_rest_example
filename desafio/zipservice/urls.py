from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^health/$', views.health_check, name='health_check'),
    url(r'^zipcode/$', views.handle_zipcode, name='handle_zipcode'),
    url(r'^zipcode/(?P<zip_code>[0-9]+)/$', views.delete_zipcode, name='delete_zipcode'),
]