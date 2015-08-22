from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
# router = DefaultRouter()
# router.register(r'enroll_session', views.enrollSession, 'enroll')

urlpatterns = patterns('',
    url(r'^access/request/(?P<membership>\d+)/$',views.accessRequest.as_view(), name="access_request"),
    url(r'^access/record/(?P<enrollid>\d+)/$',views.accessRecord.as_view(), name="access_record"),
)

# urlpatterns += router.urls

