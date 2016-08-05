from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import clubRegister, contactFormView

urlpatterns = patterns('',
    url(r'^faq/$', TemplateView.as_view(template_name='flatpages/faq.html'), name='faqURL'),
    url(r'^about/$', TemplateView.as_view(template_name='flatpages/about.html'), name='aboutURL'),
    url(r'^story/$', TemplateView.as_view(template_name='flatpages/story.html'), name='storyURL'),
    url(r'^term/$', TemplateView.as_view(template_name='flatpages/term.html'), name='termURL'),
    url(r'^contact/$', contactFormView.as_view(), name='contactURL'),
    url(r'^register/$', clubRegister.as_view(), name='clubRegisterURL'),
)

