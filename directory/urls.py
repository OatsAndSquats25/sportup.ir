from __future__ import unicode_literals
from django.views.decorators.cache import never_cache
from django.conf.urls import patterns, url
from directory import views

urlpatterns = patterns('',
    url(r'^$', never_cache(views.listAllItems.as_view()), name='directoryListAllItems'),
    #url(r'^register/$', views.clubRegistration.as_view(), name='directoryRegistration'),
    #url(r'^(?P<slug>.*)/$', views.itemDetail.as_view(), name='directoryItemDetail'),
    #url(r'^$', views.getDirectoryCategoriesList.as_view(), name='directoryCategoriesList'),
    url(r'^category/(?P<slug>.*)/$', views.getDirectoryCategoryItemList.as_view(), name='categoryList'),
    url(r'^detail/(?P<pk>.*)/(?P<locationId>\d+)/(?P<clubId>\d+)/$', views.getItemDetail.as_view(), name='itemDetail3'),
    url(r'^detail/(?P<pk>.*)/(?P<locationId>\d+)/$', views.getItemDetail.as_view(), name='itemDetail2'),
    url(r'^detail/(?P<pk>.*)/$', views.getItemDetail.as_view(), name='itemDetail1'),
)