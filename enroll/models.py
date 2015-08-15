from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from polymorphic import PolymorphicModel

from generic.models import Displayable
from program.models import programDefinition
#from finance.models import order

# ----------------------------------------------------
#class clubItemEnrollment(PolymorphicModel):

class enrolledProgram(PolymorphicModel, Displayable):
    # ENROLLMENT_STATUS_RESERVED = 1
    # ENROLLMENT_STATUS_PAYED    = 2
    # ENROLLMENT_STATUS_CANCELED = 3
    # ENROLLMENT_STATUS_REVOKED  = 4
    # ENROLLMENT_STATUS_REJECTED = 5
    # ENROLLMENT_STATUS_CHOICES = (
    #     (ENROLLMENT_STATUS_RESERVED , _("Reserved")),
    #     (ENROLLMENT_STATUS_PAYED    , _("Payed")),
    #     (ENROLLMENT_STATUS_CANCELED  , _("Canceled")),
    #     (ENROLLMENT_STATUS_REVOKED  , _("Revoked")),
    # )

    # id                  = models.AutoField(primary_key=True)
    programDefinitionKey= models.ForeignKey(programDefinition)
    invoiceKey          = models.ForeignKey('finance.invoice', blank=True, null=True)
    amount              = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)
    # enrollStatus        = models.IntegerField(_("Status"), choices= ENROLLMENT_STATUS_CHOICES, default=ENROLLMENT_STATUS_RESERVED,
    #                                           help_text=_("Please select gender if there is limitation"))

    class Meta:
        verbose_name = _('Enroll')
        verbose_name_plural = _('Enroll')

    def __unicode__(self):
        return unicode(self.programDefinitionKey)

    def reduceRemainCapacity(self):
        self.programDefinitionKey.remainCapacity -= 1

#
#    #def payingRequest(self):
#    #def payedRequest(self):
#    #def cancelRequest(self):
#    #def revokeRequest(self):
#    #def rejectRequest(self):
#
# ----------------------------------------------------
class enrolledProgramCourse(enrolledProgram):
    firstTime   = models.BooleanField(_('First time remaining flag'), default=True)

    def isValid(self):
        if self.publish_date < now() and \
           self.expiry_date > now() and \
           self.status == Displayable.CONTENT_STATUS_ACTIVE:
           return True
        return False
# ----------------------------------------------------
class enrolledProgramSession(enrolledProgram):
    date                = models.DateField(_("Specific date"))
    sessionTimeBegin    = models.TimeField(_("Begin time"))
    sessionTimeEnd      = models.TimeField(_("End time"))
# ----------------------------------------------------
