from models import invoice
from program.models import programDefinition
from enroll.models import enrolledProgram
from finance.models import transaction
from payment import testPay, payline


#----------------------------------------------------------------------
def invoiceGenerate(request, enrollInst):
    # TODO: check aginst regenerate invoice
    invoiceInst = invoice.objects.create(amount=enrollInst.amount, context='Payment pending.', user= request.user)
    enrollInst.invoiceKey = invoiceInst
    enrollInst.save()
    return invoiceInst

#----------------------------------------------------------------------
def invoicePayed(idValue):
    # change invoice`s status to active
    invoiceInst = invoice.objects.get(pk=idValue)
    invoiceInst.status = enrolledProgram.CONTENT_STATUS_ACTIVE
    invoiceInst.save()

    # change enroll`s status to active
    enrolledInst = enrolledProgram.objects.select_related().get(invoiceKey = invoiceInst)
    enrolledInst.status = enrolledProgram.CONTENT_STATUS_ACTIVE
    programInst = enrolledInst.programDefinitionKey
    enrolledInst.save()

    # Todo: check capacity and log error on zero
    # if programInst.remainCapacity == 0:

    # Reduce program capacity if it is more than 0
    if programInst.remainCapacity > 0:
        programInst.remainCapacity -= 1
        programInst.save()

    return True

#----------------------------------------------------------------------
def paymentRequest(request, invoiceInst):
    return testPay.paymentRequest(request, invoiceInst)
    return payline.paymentRequest(request, invoiceInst)

#----------------------------------------------------------------------
