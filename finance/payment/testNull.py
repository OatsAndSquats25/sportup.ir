from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def testPaymentRequest(InvoiceId):
    return redirect(reverse('financeTestGatewayURL'))

def testPaymentResponse(request,*args,**kwargs):
    res = { 'status' : True, 'invoiceId' : 1, 'context' : '---'}
    return res