from django.conf.urls import patterns, include, url

from django.contrib import admin
<<<<<<< HEAD
=======
from django.views.static import directory_index
from django.conf.urls.static import static
>>>>>>> bda1c36ba62baf38833bddb3e22dd48593346fba
from django.http import HttpResponse

admin.autodiscover()


urlpatterns = patterns('',
<<<<<<< HEAD
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
    url(r'^noadmin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include("program.urlsapi")),
    url(r'^api/', include("programsession.urlsapi")),
    url(r'^api/', include("enroll.urlsapi")),
)

urlpatterns += patterns('',
=======
    # Examples:
    # url(r'^$', 'mms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
#    url(r'^google9f49bb0345edbd3d\.html$', lambda r: HttpResponse("google-site-verification: google9f49bb0345edbd3d.html", mimetype="text/plain")),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: ", content_type="text/plain")),
>>>>>>> bda1c36ba62baf38833bddb3e22dd48593346fba
    url(r'^accounts/', include("accounts.urls")),
    url(r'^enroll/', include("enroll.urls")),
    url(r'^finance/', include("finance.urls")),
    url(r'^', include("directory.urls")),
)