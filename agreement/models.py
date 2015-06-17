from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from generic.models import Displayable
from directory.models import club
from datetime import datetime

# ----------------------------------------------------
class agreement(Displayable):
    AGREEMENT_STATUS_DRAFT    = 1
    AGREEMENT_STATUS_REQUEST  = 2
    AGREEMENT_STATUS_PROCESS  = 3
    AGREEMENT_STATUS_ACTIVE   = 4
    AGREEMENT_STATUS_PENDING  = 5
    AGREEMENT_STATUS_CANCELED = 6
    AGREEMENT_STATUS_EXPIRED  = 7
    
    AGREEMENT_STATUS_CHOICES = (
            (AGREEMENT_STATUS_DRAFT,_("Draft")),
            (AGREEMENT_STATUS_REQUEST,_("Request")),
            (AGREEMENT_STATUS_PROCESS,_("Processing")),
            (AGREEMENT_STATUS_ACTIVE,_("Active")),
            (AGREEMENT_STATUS_PENDING,_("Pending")),
            (AGREEMENT_STATUS_CANCELED,_("Canceled")),
            (AGREEMENT_STATUS_EXPIRED,_("Expired")),
    )

    clubKey             = models.ForeignKey(club)
    context             = models.TextField()
    commission          = models.DecimalField(_("Commission percentage"), default=0.05, max_digits=4, decimal_places=3)
    agreementStatus     = models.IntegerField(_("Agreement status"), choices=AGREEMENT_STATUS_CHOICES, default=AGREEMENT_STATUS_PROCESS)
    finBank             = models.CharField(_("Customer bank name"), max_length=100)
    finBranch           = models.CharField(_("Customer bank branch"), max_length=100)
    finAccount          = models.CharField(_("Customer bank account number"), max_length=100)
    finOwner            = models.CharField(_("Customer bank account owner"), max_length=100)
    finDescription      = models.CharField(_("Description"), max_length=100, blank=True, null=True)
    #userKey             = models.ManyToManyField(user_model_name, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Agreement')

    def __unicode__(self):
        return self.title

    def isValid(self):
        if self.agreementStatus == self.AGREEMENT_STATUS_ACTIVE and \
            self.publish_date < now() and \
            self.expiry_date > now():
            return True
        return False

    def remainDays(self):
        return (datetime.date(self.expiry_date) - datetime.date(datetime.now())).days
# ----------------------------------------------------