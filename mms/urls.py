from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.static import directory_index
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/', include("accounts.urls")),
    url(r'^noadmin/', include(admin.site.urls)),
    url(r'^enroll/', include("enroll.urls")),
    url(r'^finance/', include("finance.urls")),
    url(r'^', include("directory.urls")),
)
