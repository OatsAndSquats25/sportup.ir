from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
# router = DefaultRouter()
# router.register(r'enroll_session', views.enrollSession, 'enroll')

urlpatterns = patterns('',
    url(r'^enroll/session/(?P<club>\d+)/(?P<week>\d+)/(?P<id>\d+)/$',views.enrollSession.as_view(), name="Enroll_session"),
    url(r'^enroll/session/list/$',views.enrollSessionList.as_view(), name="Enroll_session_list_mine"),
    url(r'^enroll/session/list/club/(?P<agreement>\d+)/$',views.enrollSessionListClub.as_view(), name="Enroll_session_list_club"),
)

# urlpatterns += router.urls

