from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from django.core.mail import send_mail
from django.contrib import messages
# from django.core.urlresolvers import reverse

from forms import clubRegisterForm, contactForm
# -----------------------------------------------------------------------
class clubRegister(FormView):
    form_class = clubRegisterForm
    template_name = "flatpages/clubRegister.html"
    success_url = "/"

    def form_valid(self, form):
        message = "club: {name} \n owner: {owner} \n contact: {contact} \n email: {email} \n".format(
                                                    name=form.cleaned_data.get('clubName'),
                                                    owner=form.cleaned_data.get('ownerName'),
                                                    contact=form.cleaned_data.get('contact'),
                                                    email=form.cleaned_data.get('email'))
        send_mail(subject=_("SpurtUp CLUB contact form"),
                  message=message,
                  from_email='noreply@sportup.ir',
                  recipient_list=["info@sportup.ir",""],)

        messages.info(self.request,_("Thank you for filling the form. Your information has been sent to sales department."))
        return super(clubRegister, self).form_valid(form)
# -----------------------------------------------------------------------
class contactFormView(FormView):
    form_class = contactForm
    template_name = "flatpages/contact.html"
    success_url = '/pages/contact/'
    # success_url = reverse("contactFormView")

    def form_valid(self, form):
        message = "Name: {name} \n Title: {title} \n Email: {email} \n Message: {message} \n".format(
                                                    name=form.cleaned_data.get('name'),
                                                    email=form.cleaned_data.get('email'),
                                                    title=form.cleaned_data.get('title'),
                                                    message=form.cleaned_data.get('message'))
        send_mail(subject=_("SportUp contact form"),
                  message=message,
                  from_email='noreply@sportup.ir',
                  recipient_list=["info@sportup.ir",""],)

        messages.info(self.request,_("Thank you for filling the form. Your information has been sent."))
        return super(contactFormView, self).form_valid(form)
# -----------------------------------------------------------------------