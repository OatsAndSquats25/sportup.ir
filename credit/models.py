from django.db import models
from django.contrib.auth.models import User
from generic.models import Displayable
from django.utils.translation import ugettext_lazy as _

class userCredit(Displayable):
    value = models.IntegerField(_("Credit"), default=0)




