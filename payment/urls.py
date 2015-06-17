from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from payment import views

urlpatterns = patterns('',
    url(r'^request/(?P<pk>\d+)/$', login_required(views.programPaymentReq.as_view()), name='paymentRequest'),
    )

