from django import template
from django.db.models import Sum
from credit.models import userCredit

# -----------------------------------------------------------------------
def get_credit(self):
    validCredits = userCredit.objects.filter(user = self.request.user).active().aggregate(overallCredit = Sum('value'))
    return validCredits.overallCredit



