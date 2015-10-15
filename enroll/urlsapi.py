from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
# router = DefaultRouter()
# router.register(r'enroll_session', views.enrollSession, 'enroll')

urlpatterns = patterns('',
    # url(r'^enroll/session/(?P<club>\d+)/(?P<week>\d+)/(?P<id>\d+)/$',views.enrollSession.as_view(), name="Enroll_session"),
    url(r'^enroll/session/$',views.enrollSession.as_view(), name="enrollSessionAPI"),
    url(r'^enroll/session/user/$',views.enrollSessionUser.as_view(), name="enrollSessionListUserAPI"),
    url(r'^enroll/session/club/$',views.enrollSessionClub.as_view(), name="enrollSessionListClubAPI"),
    url(r'^enroll/course/club/$',views.enrollCourseClub.as_view(), name="enrollCourseListClubAPI"),
)

# urlpatterns += router.urls

