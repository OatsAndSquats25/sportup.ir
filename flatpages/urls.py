from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.views.generic import TemplateView



urlpatterns = patterns('',
    url(r'^faq/$', TemplateView.as_view(template_name='flatpages/faq.html'), name='faqURL'),
    url(r'^about/$', TemplateView.as_view(template_name='flatpages/about.html'), name='aboutURL'),
    url(r'^register/$', TemplateView.as_view(template_name='flatpages/clubRegister.html'), name='clubRegisterURL'),
    url(r'^term/$', TemplateView.as_view(template_name='flatpages/term.html'), name='termURL'),
    url(r'^contact/$', TemplateView.as_view(template_name='flatpages/contact.html'), name='contactURL'),
)

