from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache


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
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include("access.urlsapi")),
    url(r'^api/', include("agreement.urlsapi")),
    url(r'^api/', include("directory.urlsapi")),
    url(r'^api/', include("program.urlsapi")),
    url(r'^api/', include("programcourse.urlsapi")),
    url(r'^api/', include("programsession.urlsapi")),
    url(r'^api/', include("enroll.urlsapi")),
)

urlpatterns += patterns('',
    url(r'^pages/', include("flatpages.urls")),
    url(r'^credit/', include("credit.urls")),
    url(r'^accounts/', include("accounts.urls")),
    url(r'^enroll/', include("enroll.urls")),
    url(r'^checkout/', include("finance.urls")),
    url(r'^', include("directory.urls")),
    url(r'^$', never_cache(TemplateView.as_view(template_name="index.html"))),
)
