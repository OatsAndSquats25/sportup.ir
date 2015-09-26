from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from polymorphic import PolymorphicModel

from generic.models import Displayable
from program.models import programDefinition
#from finance.models import order

# ----------------------------------------------------
class enrolledProgram(PolymorphicModel, Displayable):
    programDefinitionKey= models.ForeignKey(programDefinition)
    invoiceKey          = models.ForeignKey('finance.invoice', blank=True, null=True)
    amount              = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)
    firstAccess         = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Enroll')
        verbose_name_plural = _('Enroll')

    def __unicode__(self):
        return unicode(self.programDefinitionKey)

    def reduceRemainCapacity(self):
        self.programDefinitionKey.remainCapacity -= 1

    def isValid(self):
        return self.programDefinitionKey.isValid()

    def referenceNumber(self):
        if self.invoiceKey is not None:
            return str(self.programDefinitionKey.id) + "-" + str(self.id) + "-" + str(self.invoiceKey.id)
        else:
            return str(self.programDefinitionKey.id) + "-" + str(self.id) + "-0"

# ----------------------------------------------------
class enrolledProgramCourse(enrolledProgram):
    firstTime   = models.BooleanField(_('First time remaining flag'), default=True)
# ----------------------------------------------------
class enrolledProgramSession(enrolledProgram):
    date                = models.DateField(_("Specific date"))
    sessionTimeBegin    = models.TimeField(_("Begin time"))
    sessionTimeEnd      = models.TimeField(_("End time"))
# ----------------------------------------------------
