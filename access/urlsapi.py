from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
# router = DefaultRouter()
# router.register(r'enroll_session', views.enrollSession, 'enroll')

urlpatterns = patterns('',
    url(r'^access_request/(?P<membership>\d+)/$',views.accessRequest.as_view()),
)

# urlpatterns += router.urls

