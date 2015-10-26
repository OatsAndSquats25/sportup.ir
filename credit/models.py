from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from generic.models import Displayable
from finance.models import invoice

class userCredit(Displayable):
    originValue= models.IntegerField(_("Origin Credit"), default=0)
    value      = models.IntegerField(_("Credit"), default=0)
    invoiceKey = models.ForeignKey(invoice, blank=True, null=True)




