from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
router = DefaultRouter()
router.register(r'table', views.sessionSchedule, 'sessions')

# urlpatterns = router.urls
# urlpatterns = patterns('',
#     url(r'^', include(router.urls)),
# )

urlpatterns = patterns('',
    url(r'^session_schedules/(?P<club>\d+)/(?P<week>\d+)/$',views.sessionSchedule.as_view()),
)
