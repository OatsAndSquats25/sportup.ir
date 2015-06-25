from models import invoice
from enroll.models import enrolledProgram
from payment import testNull

def invoiceGenerate(enrollInst):
    # TODO: check aginst re invoice
    invoiceInst = invoice.objects.create(paid=0, amount=enrollInst.amount, context='Payment pending.')
    enrollInst.invoiceKey = invoiceInst
    enrollInst.save()
    return invoiceInst.id

def invoicePayed(invoiceProp):
    invoiceInst = invoice.objects.get(pk=invoiceProp.invoiceInst.id)

    # invoiceProp.invoiceInst.paid = invoiceProp.paid
    # invoiceProp.invoiceInst.content = invoiceProp.ref
    # invoiceProp.invoiceInst.save()

    enrolledProgram.objects.filter(invoiceKey = invoiceInst).update(paid=True)
    return True

def invoicePayedTest(idValue):
    invoiceInst = invoice.objects.get(pk=idValue)
    invoiceInst.status = enrolledProgram.CONTENT_STATUS_ACTIVE
    invoiceInst.context = '10md4kds9934nmdids094782jkje2'
    invoiceInst.save()

    enrolledProgram.objects.filter(invoiceKey = invoiceInst).update(status=enrolledProgram.CONTENT_STATUS_ACTIVE)
    return True

def paymentRequest(invoiceId):
    return testNull.testPaymentRequest(invoiceId)
