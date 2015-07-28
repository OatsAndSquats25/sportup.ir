from django.shortcuts import render,redirect
from django.views.generic import View, TemplateView, DetailView, UpdateView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
import importlib

from registration.backends.simple.views import RegistrationView

from forms import MyRegistrationForm
from models import userProfile

User = get_user_model()
# -----------------------------------------------------------------------
class MyRegistrationView(RegistrationView):
    form_class = MyRegistrationForm

    def get_initial(self):
        return {'next': self.request.GET.get('next',self.request.POST.get('next','/'))}

    def get_success_url(self, request, user):
        messages.info(request, _("You are successfuly registered."))
        return request.POST.get('next','/')
# -----------------------------------------------------------------------
class dashboard(View):
    def get(self, request, *args, **kwargs):
        app = self.request.GET.get('app' ,None)
        cls = self.request.GET.get('cls',None)

        if app == None or cls == None:
            # app = 'accounts'
            # cls = 'homePage'
            if request.user.has_perm('accounts.club_owner'):
                app = 'program'
                cls = 'programList'
            else:
                app = 'enroll'
                cls = 'enrollList'
        try:
            mod_name = app + '.dashboard'
            mod = importlib.import_module(mod_name)
            clas = getattr(mod, cls)
        except:
            raise Http404

        return HttpResponse(clas().generate(request))
# -----------------------------------------------------------------------
class profileView(DetailView):
    template_name = 'accounts/profile_detail.html'
    model = userProfile

    def get_object(self):
        return self.model.objects.get(user = self.request.user)
# -----------------------------------------------------------------------
class profileUpdate(UpdateView):
    template_name = 'accounts/profile_update.html'
    model = userProfile
    fields = ['photo', 'nid','insurance', 'cellPhone', 'landline', 'address', 'postalcode' ]

    # def get_queryset(self):
    def get_object(self):
        try:
            return self.model.objects.get(user = self.request.user)
        except:
            return None
            # return userProfile(user =  self.request.user)

    def get_success_url(self):
        content_type = ContentType.objects.get_for_model(userProfile)
        permission = Permission.objects.get(content_type=content_type, codename='profile_is_update')

        if self.object.isUpdate() and not self.request.user.has_perm('accounts.profile_is_update'):
            self.request.user.user_permissions.add(permission)
        elif not self.object.isUpdate() and self.request.user.has_perm('accounts.profile_is_update'):
            self.request.user.user_permissions.remove(permission)

        messages.info(self.request, _("Your profile updated successfully."))
        return reverse('profileUpdate')
# -----------------------------------------------------------------------
