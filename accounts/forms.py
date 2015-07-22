from django import forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationForm
# -----------------------------------------------------------------------
class MyRegistrationForm(RegistrationForm):
    next    = forms.CharField(widget=forms.HiddenInput)
    first_name = forms.CharField(max_length = 50, label=_('first name'))
    last_name = forms.CharField(max_length = 50, label=_('last name'))

    def save(self, *args, **kwargs):
        new_user = super(MyRegistrationForm, self).save(*args, **kwargs)

        #put them on the User model instead of the profile and save the user
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()

        #get the profile fields information
        # gender = self.cleaned_data['gender']
        # ...
        # pincode = self.cleaned_data['pincode']
        #
        # #create a new profile for this user with his information
        # UserProfile(user = new_user, gender = gender, ..., pincode = pincode).save()
        #return the User model

        return new_user
# -----------------------------------------------------------------------
