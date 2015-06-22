from django.db import models
from django.utils.translation import ugettext_lazy as _

from generic.models import Displayable
from enroll.models import enrolledProgram

# Create your models here.
class enrolledProgramCourse(enrolledProgram):

    firstTime   = models.BooleanField(_('First time remaining flag'), default=True)