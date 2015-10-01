from django.apps import AppConfig
from django.db import models
from django.utils.translation import ugettext_lazy as _

#from django_jalali.db import models as jmodels
from program.models import programDefinition
# ----------------------------------------------------
VERBOSE_NAME = _('Programcourse')
# ----------------------------------------------------
class courseDefinition(programDefinition):

    USAGE_BEGIN_ENROLLMENT  = 1
    USAGE_BEGIN_FIRST_LOGIN = 2
    USAGE_BEGIN_DATE        = 3
    USAGE_BEGIN_CHOICES = (
        (USAGE_BEGIN_ENROLLMENT , _("Enrollment")),
        (USAGE_BEGIN_FIRST_LOGIN, _("First login")),
        (USAGE_BEGIN_DATE, _("Specific date")),
    )

    usageBeginChoices   = models.IntegerField(_("Usage can begin from"), choices=USAGE_BEGIN_CHOICES, default=USAGE_BEGIN_ENROLLMENT, help_text=_("Usage begin policy since enroll"))
    usageBeginDate      = models.DateField(_("Begin date of usage"), blank=True, null=True, help_text=_("Set this field if usage will start at specific date"))
    usageEndDate        = models.DateField(_("End date of usage"), blank=True, null=True, help_text=_("Set this field if usage will finish at specific date"))
    maxDays             = models.IntegerField(_("Maximum valid day"), blank=True, null=True, help_text=_("Maximum valid days since enroll choice"))
    maxSessions         = models.IntegerField(_("Maximum allowed session"), blank=True, null=True, help_text=_("Maximum sessions"))
    expireDate          = models.DateField(_("Membership expire date"), blank=True, null=True)

    class Meta:
        verbose_name = _("Course definition")
        verbose_name_plural = _("Courses definition")

    def get_absolute_url(self):
        return "Not work"
    #TODO fix this

    #def __unicode__(self):
    #    return self.agreementKey.facilityKey.complex_name() + ":" + \
    #           self.agreementKey.facilityKey.location_name() + ":"  +\
    #           self.agreementKey.facilityKey.title + ":" + self.title

    def save(self, *args, **kwargs):
        if not self.remainCapacity:
            self.remainCapacity = self.maxCapacity
        # self.reservedCapacity = 1
        if self.usageEndDate:
            if self.usageEndDate > self.agreementKey.expiry_date.date:
                self.usageEndDate = self.agreementKey.expiry_date.date
        super(courseDefinition,self).save()

# ----------------------------------------------------
class courseDays(models.Model):
    DAY_OF_WEEK_CHOICES = (
            ("SAT",_("Saturday")),
            ("SUN",_("Sunday")),
            ("MON",_("Monday")),
            ("TUE",_("Tuesday")),
            ("WED",_("Wednesday")),
            ("THU",_("Thursday")),
            ("FRI",_("Friday")),
    )

    #object              = jmodels.jManager()

    courseDefinitionKey = models.ForeignKey(courseDefinition)
    dayOfWeek           = models.CharField(_("Day of week"),max_length=3,choices=DAY_OF_WEEK_CHOICES)
    dateOfDay           = models.DateField(_("Date of day"),blank=True, null=True)
    sessionTimeBegin    = models.TimeField(_("Begin time"),blank=True, null=True)
    sessionTimeEnd      = models.TimeField(_("End time"),blank=True, null=True)

    def __unicode__(self):
        return self.courseDefinitionKey.title + "-" + self.dayOfWeek
# ----------------------------------------------------
