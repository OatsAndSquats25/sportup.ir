from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _

# -----------------------------------------------------------------------
class creditForm(forms.Form):
    value    = forms.IntegerField(label=_("value"))
# -----------------------------------------------------------------------
