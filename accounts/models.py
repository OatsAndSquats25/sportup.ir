from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import ugettext_lazy as _

#---------------------------------------------------------------------------------------------------
class userProfile(models.Model):
    user        = models.OneToOneField(User)
    photo       = models.ImageField(_("Photo"), null=True, blank=True)
    nid         = models.CharField(_("National Identity"), max_length=10, null=True, blank=True)
    insurance   = models.CharField(_("Sport`s Insurance Number"), max_length=10, null=True, blank=True)
    cellPhone   = models.CharField(_("Cell Phone"), max_length=11, null=True, blank=True, help_text=_("example: 09121231234"))
    landline    = models.CharField(_("Landline"), max_length=12, null=True, blank=True, help_text=_("With area code - example: 02122334455"))
    postalcode  = models.CharField(_("Postal Code"), max_length=10, null=True, blank=True)
    address     = models.CharField(_("Address"), max_length=400, null=True, blank=True)
    # emailAuto   = models.IntegerField()
    # membership  = models.CharField(_("Membership number"), max_length=10, unique=True) #todo

    class Meta:
        permissions = (
            ("profile_is_update", "Profile updated"),
            ("club_owner", "Club owner"),
        )

    def isUpdate(self):
        if self.user.first_name and self.user.last_name and self.photo and self.nid and self.cellPhone and self.postalcode:
            return True
        else:
            return False

    # def save(self):
    #     membership = YY,MM,DD,id
#---------------------------------------------------------------------------------------------------
#def create_user_profile(**kwargs):
#    userProfile.objects.get_or_create(user=kwargs['user'])
#---------------------------------------------------------------------------------------------------
#user_registered.connect(create_user_profile)
#---------------------------------------------------------------------------------------------------
