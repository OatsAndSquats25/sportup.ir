from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
# router = DefaultRouter()
# router.register(r'enroll_session', views.enrollSession, 'enroll')

urlpatterns = patterns('',
    url(r'^enroll_session/$',views.enrollSessionList.as_view()),
    url(r'^enroll_session_create/$',views.enrollSessionCreate.as_view()),
)

# urlpatterns += router.urls

