from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from views import MyRegistrationView, dashboard, profileView, profileUpdate

urlpatterns = patterns('',
    url(r'^register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^', include('registration.backends.simple.urls')),
    url(r'^dashboard/$', login_required(dashboard.as_view()), name='dashboard'),
    url(r'^$', login_required(profileView.as_view()), name='profileView'),
    url(r'^update/$', login_required(profileUpdate.as_view()), name='profileUpdate'),
    #url(r'^', include('registration.backends.default.urls')),
    #url(r'^', include('    django.contrib.auth.urls')),
)