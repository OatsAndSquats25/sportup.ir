from django.db import models
from django.utils.translation import ugettext_lazy as _

from polymorphic import PolymorphicModel

from polymorphic import PolymorphicModel

from generic.models import Displayable
from program.models import programDefinition
#from finance.models import order

# ----------------------------------------------------
#class clubItemEnrollment(PolymorphicModel):

class enrolledProgram(PolymorphicModel, Displayable):

    ENROLLMENT_STATUS_RESERVED = 1
    ENROLLMENT_STATUS_PAYED    = 2
    ENROLLMENT_STATUS_CANCELED = 3
    ENROLLMENT_STATUS_REVOKED  = 4
    ENROLLMENT_STATUS_REJECTED = 5
    ENROLLMENT_STATUS_CHOICES = (
        (ENROLLMENT_STATUS_RESERVED , _("Reserved")),
        (ENROLLMENT_STATUS_PAYED    , _("Payed")),
        (ENROLLMENT_STATUS_CANCELED  , _("Canceled")),
        (ENROLLMENT_STATUS_REVOKED  , _("Revoked")),
    )

    # id                  = models.AutoField(primary_key=True)
    programDefinitionKey= models.ForeignKey(programDefinition)
    invoiceKey          = models.ForeignKey('finance.invoice', default=0)
    amount              = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)
    # enrollStatus        = models.IntegerField(_("Status"), choices= ENROLLMENT_STATUS_CHOICES, default=ENROLLMENT_STATUS_RESERVED,
    #                                           help_text=_("Please select gender if there is limitation"))

    class Meta:
        verbose_name = _('enroll')
        verbose_name_plural = _('Enroll')

    def __unicode__(self):
        return unicode(self.programDefinitionKey)
#
#    #def payingRequest(self):
#    #def payedRequest(self):
#    #def cancelRequest(self):
#    #def revokeRequest(self):
#    #def rejectRequest(self):
#
## ----------------------------------------------------