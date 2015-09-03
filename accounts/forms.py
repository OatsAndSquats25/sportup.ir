from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
# from registration.forms import RegistrationForm

User = get_user_model()
# -----------------------------------------------------------------------
# class MyRegistrationForm(RegistrationForm):
#     next    = forms.CharField(widget=forms.HiddenInput)
#     first_name = forms.CharField(max_length = 50, label=_('first name'))
#     last_name = forms.CharField(max_length = 50, label=_('last name'))
#
#     def save(self, *args, **kwargs):
#         new_user = super(MyRegistrationForm, self).save(*args, **kwargs)
#
#         #put them on the User model instead of the profile and save the user
#         new_user.first_name = self.cleaned_data['first_name']
#         new_user.last_name = self.cleaned_data['last_name']
#         new_user.save()
#
#         #get the profile fields information
#         # gender = self.cleaned_data['gender']
#         # ...
#         # pincode = self.cleaned_data['pincode']
#         #
#         # #create a new profile for this user with his information
#         # UserProfile(user = new_user, gender = gender, ..., pincode = pincode).save()
#         #return the User model
#
#         return new_user
# -----------------------------------------------------------------------
class userRegisterForm(forms.Form):
    email       = forms.EmailField(label=_("Email"))
    password    = forms.CharField(widget=forms.PasswordInput(), label=_("Password"))
    first_name  = forms.CharField(max_length=30, label=_("first name"))
    last_name   = forms.CharField(max_length=30, label=_("last name"))

    def is_valid(self):
        valid = super(userRegisterForm, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        emailData = self.cleaned_data.get('email')
        try:
            userInst = User.objects.get(email = emailData)

        # no user with this username or email address
        except User.DoesNotExist:
            return True

        # raise forms.ValidationError(_('Email address exist.'), code='email_duplicate',)
        return False

    def clean(self):
        cleaned_data = super(userRegisterForm, self).clean()
        emailData = cleaned_data.get('email', None)
        if emailData is not None:
            try:
                userInst = User.objects.get(email = emailData)
            except User.DoesNotExist:
                return self.cleaned_data
            raise forms.ValidationError(_('Email address exist.'), code='email_duplicate',)
# -----------------------------------------------------------------------
class userLoginForm(forms.Form):
    email   = forms.EmailField(label=_("Email"))
    password= forms.CharField(widget=forms.PasswordInput(), label=_("Password"))
# -----------------------------------------------------------------------
