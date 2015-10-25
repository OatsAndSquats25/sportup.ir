from __future__ import unicode_literals

from django.conf.urls import patterns, url

from credit.views import addCredit

urlpatterns = patterns('',
    url(r'^$', addCredit.as_view(), name='addCreditURL')
    )

