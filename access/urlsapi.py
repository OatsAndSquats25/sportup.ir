from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
# router = DefaultRouter()
# router.register(r'enroll_session', views.enrollSession, 'enroll')

urlpatterns = patterns('',
    url(r'^access/$',views.accessView.as_view(), name="accessAPI"),
    url(r'^access/request/$',views.accessRequest.as_view(), name="accessUserAPI"),
)

# urlpatterns += router.urls

