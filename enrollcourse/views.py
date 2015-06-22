from django.shortcuts import render

from program.models import programDefinition
from enrollcourse.models import enrolledProgramCourse
from finance.models import invoice
# Create your views here.

def enrollCourse(request, *args, **kwargs):
    programInst = programDefinition.objects.get(pk=kwargs['pk'])
    invoiceInst = invoice.objects.create(paid=0,
                                         amount=programInst.price,
                                         context='request for payment...')
    enrolledProgramCourseInst = enrolledProgramCourse.objects.create(programDefinitionKey=programInst,
                                                                     invoiceKey= invoiceInst,
                                                                     amount= programInst.price,
                                                                     publish_date= programInst.publish_date,
                                                                     expiry_date= programInst.expiry_date)
    return enrolledProgramCourseInst.id