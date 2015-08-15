from django.conf.urls import patterns, include, url

from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
router = DefaultRouter()
router.register(r'info', views.programInformation, 'program')

# urlpatterns = router.urls
# urlpatterns = patterns('',
#     url(r'^', include(router.urls)),
# )

urlpatterns = patterns('',
    url(r'^program_info/(?P<pk>\d+)/$',views.programInformation.as_view()),
    )
