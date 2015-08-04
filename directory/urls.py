from __future__ import unicode_literals
from django.views.decorators.cache import never_cache
from django.conf.urls import patterns, url
from directory import views

urlpatterns = patterns('',
        url(r'^$', never_cache(views.listAllItems.as_view()), name='directoryListAllItems'),
        url(r'^register/$', views.clubRegistration.as_view(), name='directoryRegistration'),
        url(r'^(?P<slug>.*)/$', views.itemDetail.as_view(), name='directoryItemDetail'),
        )