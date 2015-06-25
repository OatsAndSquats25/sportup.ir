from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView
from django.http import HttpResponse

from registration.backends.simple.views import RegistrationView
from registration.forms import RegistrationForm
from django import forms

# Create your views here.
class MyRegistrationForm(RegistrationForm):
    next    = forms.CharField(widget=forms.HiddenInput)

class MyRegistrationView(RegistrationView):
    form_class = MyRegistrationForm

    def get_initial(self):
        return {'next': self.request.GET.get('next',self.request.POST.get('next','/'))}

    def get_success_url(self, request, user):
        return request.POST.get('next','/')

class dashboard(TemplateView):
    template_name = 'registration/dashboard.html'