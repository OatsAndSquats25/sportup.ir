from django import template
from datetime import datetime,time
import jdatetime


register = template.Library()
# -----------------------------------------------------------------------
@register.filter
def g2j(gregorian):
    if isinstance(gregorian, time):
        return jdatetime.date.fromgregorian(date=gregorian)
    elif isinstance(gregorian, datetime):
        return jdatetime.date.fromgregorian(date=gregorian.date())
    else:
        return gregorian
# -----------------------------------------------------------------------
@register.filter
def g2jdate(gregorian):
    return jdatetime.date.fromgregorian(date=gregorian)
# -----------------------------------------------------------------------
@register.filter
def g2jdatetime(gregorian):
    return jdatetime.datetime.fromgregorian(datetime=gregorian)
# -----------------------------------------------------------------------
