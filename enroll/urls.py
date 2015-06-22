from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from enroll import views

urlpatterns = patterns('',
    url(r'^confirm/(?P<pk>\d+)/$', login_required(views.enrollmentConfirmation.as_view()), name='enrollmentConfirmation'),
    #url(r'^$', views.enrollmentList.as_view(), name='enrollmentListURL'),
    #url(r'^list/(?P<agreementId>\d+)/(?P<programId>\d+)/$', views.enrollmentList2.as_view(), name='enrollmentListURL2'),
    )

