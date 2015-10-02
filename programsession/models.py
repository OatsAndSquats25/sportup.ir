from django.db import models
from django.utils.translation import ugettext_lazy as _

from program.models import programDefinition

# ----------------------------------------------------
class sessionDefinition(programDefinition):
    sessionTimeBegin    = models.TimeField(_("Begin time"),blank=True, null=True)
    sessionTimeEnd      = models.TimeField(_("End time"),blank=True, null=True)
    sessionDuration     = models.TimeField(_("Session duration"))
    # sessionGap          = models.TimeField(_("Gap between sessions"))
    daySat              = models.BooleanField(_("Saturday"))
    daySun              = models.BooleanField(_("Sunday"))
    dayMon              = models.BooleanField(_("Monday"))
    dayTue              = models.BooleanField(_("Tuesday"))
    dayWed              = models.BooleanField(_("Wednesday"))
    dayThu              = models.BooleanField(_("Thursday"))
    dayFri              = models.BooleanField(_("Friday"))
    daysToShow          = models.IntegerField(_("Number of next days to show"), default=7)

    class Meta:
        verbose_name =_("Definition")
        verbose_name_plural =_("Definitions")

    def __unicode__(self):
        return self.title
# ----------------------------------------------------
class sessionRestriction(models.Model):
    sessionDefinitionKey    = models.ForeignKey(sessionDefinition)
    date                = models.DateField(_("Specific date"),blank=True, null=True)
    day                 = models.IntegerField(_("Day of week"),blank=True, null=True)
    sessionTimeBegin    = models.TimeField(_("Begin time"),blank=True, null=True)
    sessionTimeEnd      = models.TimeField(_("End time"),blank=True, null=True)
    capacityDiff        = models.IntegerField(_("Capacity Increase/Decrease"),blank=True, null=True)
    blackout            = models.BooleanField(_("Blockout"))

    class Meta:
        verbose_name =_("Restriction")
        verbose_name_plural =_("Restrictions")
# ----------------------------------------------------


