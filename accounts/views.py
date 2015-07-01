from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView
from django.http import HttpResponse, Http404
import importlib

from registration.backends.simple.views import RegistrationView
from registration.forms import RegistrationForm
from django import forms

# -----------------------------------------------------------------------
class MyRegistrationForm(RegistrationForm):
    next    = forms.CharField(widget=forms.HiddenInput)
# -----------------------------------------------------------------------
class MyRegistrationView(RegistrationView):
    form_class = MyRegistrationForm

    def get_initial(self):
        return {'next': self.request.GET.get('next',self.request.POST.get('next','/'))}

    def get_success_url(self, request, user):
        return request.POST.get('next','/')
# -----------------------------------------------------------------------
class dashboard(View):
    def get(self, request, *args, **kwargs):
        app = self.request.GET.get('app' ,None)
        cls = self.request.GET.get('cls',None)

        if app == None or cls == None:
            app = 'accounts'
            cls = 'homePage'

        try:
            mod_name = app + '.dashboard'
            mod = importlib.import_module(mod_name)
            clas = getattr(mod, cls)
        except:
            return Http404

        return HttpResponse(clas().generate())
# -----------------------------------------------------------------------
# class dashboard(TemplateView):
#     template_name = 'dashboard/dashboard.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(dashboard, self).get_context_data(**kwargs)
#         app = self.request.GET.get('app' ,None)
#         cls = self.request.GET.get('cls',None)
#
#         if app == None or cls == None:
#             app = 'accounts'
#             cls = 'homePage'
#
#         try:
#             mod_name = app + '.dashboard'
#             mod = importlib.import_module(mod_name)
#             clas = getattr(mod, cls)
#         except:
#             return Http404
#
#         context['body'] = clas().generate()
#         return context
# -----------------------------------------------------------------------