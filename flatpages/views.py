from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib import messages

from forms import clubRegisterForm
# -----------------------------------------------------------------------
class clubRegister(FormView):
    form_class = clubRegisterForm
    template_name = "flatpages/clubRegister.html"
    success_url = "/"

    def form_valid(self, form):
        message = "{name} / {email} said: ".format( name=form.cleaned_data.get('clubName'),
                                                    owner=form.cleaned_data.get('ownerName'),
                                                    contact=form.cleaned_data.get('contact'),
                                                    email=form.cleaned_data.get('email'))
        send_mail(subject=_("New club request form"),
                  message=message,
                  from_email='noreply@sportup.ir',
                  recipient_list=["info@sportup.ir",""],)

        messages.info(self.request,_("Thank you for filling the form. Your information has beed send to sales department."))
        return super(clubRegister, self).form_valid(form)