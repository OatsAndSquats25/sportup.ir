from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
# router = DefaultRouter()
# router.register(r'enroll_session', views.enrollSession, 'enroll')

urlpatterns = patterns('',
    url(r'^access/request/$',views.accessRequest.as_view(), name="access_request"),
    url(r'^access/record/$',views.accessRecord.as_view(), name="access_record"),
)

# urlpatterns += router.urls

