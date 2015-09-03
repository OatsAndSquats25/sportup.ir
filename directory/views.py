from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

# from accounts.views import MyRegistrationView
from generic.models import Displayable
from models import club
from forms import clubRegistrationForm

# -----------------------------------------------------------------------
class listAllItems(ListView):
    template_name = "directory/listall.html"
    model = club

    def get_queryset(self):
        return self.model.objects.filter(status = Displayable.CONTENT_STATUS_ACTIVE)
# -----------------------------------------------------------------------
class itemDetail(DetailView):
    template_name = "directory/item.html"
    model = club
# -----------------------------------------------------------------------
# class clubRegistration(MyRegistrationView):
#     template_name = 'directory/club_registration.html'
#     form_class = clubRegistrationForm
# -----------------------------------------------------------------------