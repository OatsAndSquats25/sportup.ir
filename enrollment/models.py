from django.db import models
from django.utils.translation import ugettext_lazy as _

from program.models import programDefinition
#from finance.models import order

# ----------------------------------------------------
class clubItemEnrollment(models.Model):

    ENROLLMENT_STATUS_RESERVED = 1
    ENROLLMENT_STATUS_PAYING   = 2
    ENROLLMENT_STATUS_PAYED    = 3
    ENROLLMENT_STATUS_CANCELED = 4
    ENROLLMENT_STATUS_REVOKED  = 5
    ENROLLMENT_STATUS_REJECTED = 6
    ENROLLMENT_STATUS_CHOICES = (
        (ENROLLMENT_STATUS_RESERVED , _("Reserved")),
        (ENROLLMENT_STATUS_PAYED  , _("Payed")),
        (ENROLLMENT_STATUS_CANCELED  , _("Canceled")),
        (ENROLLMENT_STATUS_REVOKED  , _("Revoked")),
    )

    id                  = models.AutoField(primary_key=True)
    clubItemDefinitionKey= models.ForeignKey(programDefinition)
    invoiceKey          = models.ForeignKey('finance.invoice', default=0)
    amount              = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)
    status              = models.IntegerField(_("Status"), choices= ENROLLMENT_STATUS_CHOICES, help_text=_("Please select gender if there is limitation"))

    class Meta:
        verbose_name = _('enrollment')
        verbose_name_plural = _('Enrollment')

    def __unicode__(self):
        return unicode(self.clubItemDefinitionKey)
#
#    #def payingRequest(self):
#    #def payedRequest(self):
#    #def cancelRequest(self):
#    #def revokeRequest(self):
#    #def rejectRequest(self):
#
## ----------------------------------------------------
