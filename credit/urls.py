from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from credit.views import addCredit

urlpatterns = patterns('',
    url(r'^$', login_required(addCredit.as_view()), name='addCreditURL')
    )

