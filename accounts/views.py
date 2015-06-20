from django.shortcuts import render,redirect
from django.views.generic import View

from registration.backends.simple.views import RegistrationView


# Create your views here.
class MyRegistrationView(RegistrationView):
    def register(self, request, form):
        request.POST.get('next', request.GET.get('next','/'))
        super(MyRegistrationView, self).register(self, request, form)