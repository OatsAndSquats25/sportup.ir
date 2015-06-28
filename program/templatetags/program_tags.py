#from __future__ import unicode_literals
from django import template
from django.utils.translation import ugettext_lazy as _

from agreement.models import agreement
from program.models import programDefinition

register = template.Library()
# ----------------------------------------------------
@register.inclusion_tag('program/program_list_tag.html')
def program_list(id):
    currentAgreement = agreement.objects.get(clubKey = id)

    if not currentAgreement.isValid():
        return ''

    definedCourses = programDefinition.objects.filter(agreementKey = currentAgreement)

    return {'object_list' : definedCourses}
# ----------------------------------------------------
