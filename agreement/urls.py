from __future__ import unicode_literals

from django.conf.urls import patterns, url

from agreement import views

urlpatterns = patterns('',
    url(r'^$', views.agreementList.as_view(), name='agreementListURL'),
    url(r'^request/(?P<facilityId>\d+)/$', views.agreementRequest.as_view(), name='agreementRequestURL'),
    url(r'^requestwizard/(?P<facilityId>\d+)/$', views.agreementRequestWizard.as_view(), name='agreementRequestWizardURL'),
    url(r'^success/$', views.success.as_view(), name='agreementSuccessURL')
    )

