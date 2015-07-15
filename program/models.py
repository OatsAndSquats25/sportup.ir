from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from polymorphic import PolymorphicModel

from generic.models import Displayable
from directory.models import club
from agreement.models import agreement

#from datetime import datetime

# ----------------------------------------------------
class programDefinition(PolymorphicModel, Displayable):

    TYPE_COURSE = 1
    TYPE_SESSION = 2

    GENDER_BOTH   = 1
    GENDER_MALE   = 2
    GENDER_FEMALE = 3
    GENDER_CHOICES = (
        (GENDER_BOTH , _("Male/Female")),
        (GENDER_MALE , _("Male")),
        (GENDER_FEMALE  , _("Female")),
    )

    agreementKey        = models.ForeignKey(agreement, verbose_name=_('Agreement'))
    #coachUserKey        = models.ManyToManyField(user_model_name, blank=True, null=True)
    maxCapacity         = models.IntegerField(_("Maximum capacity"), default=-1, help_text=_("Please fill if your program has maximum capacity"))
    remainCapacity      = models.IntegerField(_("Remain capacity"), blank=True, null=True)
    price               = models.DecimalField(_("Price"), max_digits=15, decimal_places=0)
    ageMin              = models.IntegerField(_("Age minimum"), default=0)
    ageMax              = models.IntegerField(_("Age maximum"), default=100)
    genderLimit         = models.IntegerField(_("Gender"), choices= GENDER_CHOICES, default=GENDER_BOTH, help_text=_("Please select gender if there is limitation"))
    needInsurance       = models.BooleanField(_("Sport insurance required"), default=False, help_text=_("Mark if your program needs sport insurance"))
    multipleReserve     = models.BooleanField(_("Multiple reserve eligibility"), default=False, help_text=_("Mark if you want to permit each account can reserve multiple instance of this program"))

    def clubSlug(self):
        return self.agreementKey.clubKey.slug

    #or self.agreementKey.expiry_date > datetime.now()
    def isValid(self):
        if self.agreementKey.isValid() and \
           self.publish_date < now() and \
           self.expiry_date > now() and \
           self.remainCapacity != 0 and \
           self.status == Displayable.CONTENT_STATUS_ACTIVE:
            return True
        return False

    def __unicode__(self):
        #return self.agreementKey.facilityKey + "-" + self.title +"-"+ self.agreementKey.id
        return self.title
# ----------------------------------------------------
