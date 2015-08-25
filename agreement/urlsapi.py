from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
# router = DefaultRouter()
# router.register(r'enroll_session', views.enrollSession, 'enroll')

urlpatterns = patterns('',
    url(r'^agreement/list/$',views.agreementList.as_view(), name= "agreementListAPI"),
    url(r'^agreement/clubs/$',views.agreementClubs.as_view(), name= "agreementClubsAPI"),
)

# urlpatterns += router.urls

