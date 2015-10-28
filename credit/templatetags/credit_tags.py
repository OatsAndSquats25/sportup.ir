from django import template
from django.db.models import Sum
from credit.models import userCredit

register = template.Library()

# -----------------------------------------------------------------------
@register.simple_tag(takes_context=True)
def get_credit(context):
    request = context['request']
    validCredits = userCredit.objects.active().filter(user = request.user).aggregate(overallCredit = Sum('value'))
    if validCredits['overallCredit']:
        return validCredits['overallCredit']
    else:
        return 0
# -----------------------------------------------------------------------
