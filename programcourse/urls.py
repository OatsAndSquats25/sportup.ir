from __future__ import unicode_literals

from django.conf.urls import patterns, url
from course import views

urlpatterns = patterns('',
    url(r'^$', views.courseList.as_view(), name='courseListURL'),
    url(r'^all/$', views.courseList.as_view(), {'listAll':True}, name='courseListAllURL'),
    url(r'^toggle/(?P<agreementId>\d+)/(?P<courseId>\d+)/(?P<status>.*)/$', views.courseToggleStatus.as_view(), name='courseToggleURL'),
    url(r'^add/(?P<agreementId>\d+)/$', views.courseAddCopy.as_view(), name='courseAddURL1'),
    url(r'^add/(?P<agreementId>\d+)/(?P<categoryTitle>.*)/$', views.courseAddCopy.as_view(), name='courseAddURL2'),
    url(r'^copy/(?P<agreementId>\d+)/(?P<courseId>\d+)/$', views.courseAddCopy.as_view(), name='courseCopyURL'),
    url(r'^reserve/(?P<courseId>\d+)/$', views.courseReserve.as_view(), name='courseReserveURL'), #TODO it is good to move this link to common
    url(r'^category/$', views.categorySearch.as_view(), name='courseCategorySearchURL'),
    )

