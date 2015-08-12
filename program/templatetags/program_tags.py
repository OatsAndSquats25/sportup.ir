#from __future__ import unicode_literals
from django import template
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from agreement.models import agreement
from program.models import programDefinition
from programcourse.models import courseDefinition

register = template.Library()
# ----------------------------------------------------
@register.inclusion_tag('program/program_list_tag.html')
def program_list(id):
    try:
        currentAgreement = agreement.objects.get(clubKey = id)
    except ObjectDoesNotExist:
        return {}

    if not currentAgreement.isValid():
        return {}

    definedCourses = programDefinition.objects.instance_of(courseDefinition).filter(agreementKey = currentAgreement)

    return {'object_list' : definedCourses}
# ----------------------------------------------------
