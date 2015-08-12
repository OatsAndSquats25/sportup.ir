from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.static import directory_index
from django.conf.urls.static import static
from django.http import HttpResponse

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#    url(r'^google9f49bb0345edbd3d\.html$', lambda r: HttpResponse("google-site-verification: google9f49bb0345edbd3d.html", mimetype="text/plain")),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", mimetype="text/plain")),
    url(r'^accounts/', include("accounts.urls")),
    url(r'^noadmin/', include(admin.site.urls)),
    url(r'^enroll/', include("enroll.urls")),
    url(r'^finance/', include("finance.urls")),
    url(r'^', include("directory.urls")),
)
