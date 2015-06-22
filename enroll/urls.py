from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from enroll import views

urlpatterns = patterns('',
    url(r'^confirm/(?P<pk>\d+)/$', login_required(views.enrollConfirmation.as_view()), name='enrollConfirmation'),
    url(r'^confirmed/(?P<pk>\d+)/$', login_required(views.enrollConfirmed.as_view()), name='enrollConfirmed'),
    #url(r'^$', views.enrollmentList.as_view(), name='enrollmentListURL'),
    #url(r'^list/(?P<agreementId>\d+)/(?P<programId>\d+)/$', views.enrollmentList2.as_view(), name='enrollmentListURL2'),
    )

