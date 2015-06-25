from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from finance import views

urlpatterns = patterns('',
    # url(r'^order/$', views.financeOrder.as_view(), name='financeOrderURL'),
    # url(r'^deleteitem/(?P<pk>\d+)/$', views.fianceDeleteItem.as_view(), name='financeDeleteItem'),
    url(r'^paymentresponse/$', csrf_exempt(views.paymentResponse.as_view()), name='financePaymentResponseURL'),
    )

