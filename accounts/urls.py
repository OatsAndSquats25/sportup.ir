from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from views import dashboard, profileUpdate, loginRegister, emailTest, smsTest, dashboardSelector, printForUser, loginRegisterCampaign, welcome

urlpatterns = patterns('',
   url(r'^loginregister/$', loginRegister.as_view(), name='accountsLoginRegister'),
   url(r'^login/$', loginRegisterCampaign.as_view(), name='accountsLoginURL'),
   url(r'^register/$', loginRegisterCampaign.as_view(), {'register': True}, name='accountsRegisterURL'),
   url(r'^print/(?P<pk>\d+)/$', login_required(printForUser.as_view()), name='print'),
   url(r'^dashboard/$', login_required(dashboardSelector.as_view()), name='dashboardURL'),
   url(r'^profile/$', login_required(profileUpdate.as_view()), name='profileUpdate'),
   url(r'^', include('django.contrib.auth.urls')),
   url(r'^welcome/$', welcome.as_view(), name='welcomeURL'),
   #url(r'^email/$', login_required(emailTest.as_view()), name='emailURL'),
   #url(r'^sms/$', login_required(smsTest.as_view()), name='smsURL'),
)