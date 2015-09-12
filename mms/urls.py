from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
    url(r'^noadmin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^api/docs/', include('rest_framework_swagger.urls')),
    )

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include("access.urlsapi")),
    url(r'^api/', include("agreement.urlsapi")),
    url(r'^api/', include("directory.urlsapi")),
    url(r'^api/', include("program.urlsapi")),
    url(r'^api/', include("programsession.urlsapi")),
    url(r'^api/', include("enroll.urlsapi")),
)

urlpatterns += patterns('',
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
    url(r'^accounts/', include("accounts.urls")),
    url(r'^enroll/', include("enroll.urls")),
    url(r'^checkout/', include("finance.urls")),
    url(r'^', include("directory.urls")),
)
