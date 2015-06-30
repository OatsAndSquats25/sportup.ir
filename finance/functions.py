from models import invoice
from program.models import programDefinition
from enroll.models import enrolledProgram
from finance.models import transaction
from payment import testPay, payline


#----------------------------------------------------------------------
def invoiceGenerate(request, enrollInst):
    # TODO: check aginst re invoice
    invoiceInst = invoice.objects.create(amount=enrollInst.amount, context='Payment pending.', user= request.user)
    enrollInst.invoiceKey = invoiceInst
    enrollInst.save()
    return invoiceInst

#----------------------------------------------------------------------
def invoicePayed(idValue):
    invoiceInst = invoice.objects.get(pk=idValue)
    invoiceInst.status = enrolledProgram.CONTENT_STATUS_ACTIVE
    invoiceInst.save()

    enrolledInst = enrolledProgram.objects.select_related().get(invoiceKey = invoiceInst)
    enrolledInst.status = enrolledProgram.CONTENT_STATUS_ACTIVE
    programInst = enrolledInst.programDefinitionKey
    enrolledInst.save()
    programInst.remainCapacity -= 1
    programInst.save()

    return True

#----------------------------------------------------------------------
def paymentRequest(request, invoiceInst):
    return testPay.paymentRequest(request, invoiceInst)
    return payline.paymentRequest(request, invoiceInst)

#----------------------------------------------------------------------
