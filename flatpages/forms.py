from django import forms
from django.utils.translation import ugettext_lazy as _

# -----------------------------------------------------------------------
class clubRegisterForm(forms.Form):
    clubName    = forms.CharField(label=_("Club"))
    ownerName   = forms.CharField(label=_("last name"))
    contact     = forms.CharField(label=_("Cell Phone"))
    email       = forms.CharField(label=_("Email"), required=False)
