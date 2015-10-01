from django.conf.urls import patterns, include, url

# from rest_framework.routers import DefaultRouter

import views

# ----------------------------------------------------
# router = DefaultRouter()
# router.register(r'info', views.programInformation, 'program')

# urlpatterns = router.urls
# urlpatterns = patterns('',
#     url(r'^', include(router.urls)),
# )

urlpatterns = patterns('',
    url(r'^directory/fav/$',views.getFav.as_view(), name="directoryFavAPI"),
    url(r'^directory/(?P<pk>\d+)/$',views.getItem.as_view(), name="directoryItemAPI"),
    url(r'^directory/',views.getList.as_view(), name="directoryAPI"),
    )
