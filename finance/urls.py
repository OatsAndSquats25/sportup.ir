from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required

from finance.views import checkout, fianceDeleteItem, paymentResponse, testGateway, checkoutPay, paymentSucceeded, paymentFailed

urlpatterns = patterns('',
    url(r'^$', login_required(checkout.as_view()), name='checkoutURL'),
    url(r'^pay/$', login_required(checkoutPay.as_view()), name='checkoutPayURL'),
    url(r'^deleteitem/(?P<pk>\d+)/$', login_required(fianceDeleteItem.as_view()), name='checkoutDeleteItem'),
    url(r'^paymentresponse/(?P<gateway>.*)/$', csrf_exempt(paymentResponse.as_view()), name='financePaymentResponseURL1'),
    url(r'^paymentresponse/(?P<gateway>.*)/(?P<additional>.*)$', csrf_exempt(paymentResponse.as_view()), name='financePaymentResponseURL2'),
    url(r'^testgateway/(?P<refid>\d+)/$', testGateway.as_view(), name = 'financeTestGatewayURL'),
    url(r'^paymentSucceeded/$', login_required(paymentSucceeded.as_view()), name='paymentSucceededURL'),
    url(r'^paymentFailed/$', login_required(paymentFailed.as_view()), name='paymentFailedURL'),
    )

