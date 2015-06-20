from django.conf.urls import patterns, include, url

from views import MyRegistrationView

urlpatterns = patterns('',
    url(r'^register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^', include('registration.backends.simple.urls')),
    #url(r'^', include('registration.backends.default.urls')),
    #url(r'^', include('django.contrib.auth.urls')),
)