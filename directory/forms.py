from django import forms
from django.utils.translation import ugettext_lazy as _

from directory.models import club
from registration.forms import RegistrationForm

# -----------------------------------------------------------------------
class clubForm(forms.ModelForm):
    class Meta:
        model = club
        fields = ['title','summary','detail','address','website','phone','cell','logo']
# -----------------------------------------------------------------------
# class clubRegistrationForm(RegistrationForm, clubForm):
class clubRegistrationForm(RegistrationForm):
    title   = forms.CharField(label=_("Title"), max_length=50)
    summary = forms.CharField(label=_("Summary"), max_length=200, widget=forms.Textarea)
    detail  = forms.CharField(label=_("Description"), widget=forms.Textarea)
    address = forms.CharField(label=_("Address"), max_length=200)
    website = forms.CharField(label=_("Website"), max_length=100)
    phone   = forms.CharField(label=_("Photo"), max_length=20)
    cell    = forms.CharField(label=_("Cell"), max_length=20)
    logo    = forms.ImageField(label=_("Logo"), ) #height=200, width=350
    next    = forms.CharField(widget=forms.HiddenInput)

    def save(self, *args, **kwargs):
        new_user = super(clubRegistrationForm, self).save(*args, **kwargs)
        club(user = new_user,
        title  = self.cleaned_data['title'],
        summary  = self.cleaned_data['summary'],
        detail   = self.cleaned_data['detail'],
        address  = self.cleaned_data['address'],
        website  = self.cleaned_data['website'],
        phone    = self.cleaned_data['phone'],
        cell     = self.cleaned_data['cell'],
        logo     = self.cleaned_data['logo']).save()
        return new_user
# -----------------------------------------------------------------------