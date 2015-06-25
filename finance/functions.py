from models import invoice
from payment import testNull

def invoiceGenerate(enrollInst):
    # TODO: check aginst re invoice
    invoiceInst = invoice.objects.create(paid=0, amount=enrollInst.amount, context='Payment pending.')
    enrollInst.invoiceKey = invoiceInst
    enrollInst.save()
    return invoiceInst.id

def invoicePayed(invoiceProp):
    invoiceInst = invoice.objects.get(pk=invoiceProp.invoiceInst.id)
    invoiceProp.invoiceInst.paid = invoiceProp.paid
    invoiceProp.invoiceInst.content = invoiceProp.ref
    invoiceProp.invoiceInst.save()
    return True


def paymentRequest(invoiceId):
    return testNull.testPaymentRequest(invoiceId)
