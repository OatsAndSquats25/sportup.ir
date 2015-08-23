from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from finance import views

urlpatterns = patterns('',
    url(r'^$', views.checkout.as_view(), name='checkoutURL'),
    url(r'^pay/$', views.checkout.as_view(), {'command':'pay'}, name='checkoutPayURL'),
    url(r'^deleteitem/(?P<pk>\d+)/$', views.fianceDeleteItem.as_view(), name='checkoutDeleteItem'),
    url(r'^paymentresponse/(?P<gateway>.*)/$', csrf_exempt(views.paymentResponse.as_view()), name='financePaymentResponseURL1'),
    url(r'^paymentresponse/(?P<gateway>.*)/(?P<additional>.*)$', csrf_exempt(views.paymentResponse.as_view()), name='financePaymentResponseURL2'),
    url(r'^testgateway/(?P<refid>\d+)/$', views.testGateway.as_view(), name = 'financeTestGatewayURL'),
    )

