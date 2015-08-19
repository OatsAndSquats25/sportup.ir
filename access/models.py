from django.db import models

from generic.models import Displayable

from enroll.models import enrolledProgram
#---------------------------------------------------------------------------------------------------
class access(Displayable):
    enrollKey   = models.ForeignKey(enrolledProgram)
    # user        = models.ForeignKey(user)
    datetime    = models.DateTimeField()

#---------------------------------------------------------------------------------------------------
