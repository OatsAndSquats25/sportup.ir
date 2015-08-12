from __future__ import unicode_literals

from django.conf.urls import patterns, url, include
from programsession import views
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'session', views.sessionSchedule,'se')

urlpatterns = patterns('',
    url(r'^$',views.sessionSchedule.as_view()),
    # url(r'^', include(router.urls)),
    )

# urlpatterns += router.urls