from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from views import dashboard, profileUpdate, loginRegister, emailTest, smsTest, dashboardSelector

urlpatterns = patterns('',

    url(r'^login/$', loginRegister.as_view(), name='accounts_login_register'),
    url(r'^dashboard/$', login_required(dashboardSelector.as_view()), name='dashboard'),
    url(r'^profile/$', login_required(profileUpdate.as_view()), name='profileUpdate'),
    # url(r'^', include('registration.backends.simple.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^email/$', login_required(emailTest.as_view()), name='emailURL'),
    url(r'^sms/$', login_required(smsTest.as_view()), name='smsURL'),
)