from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def xxxPaymentRequest(InvoiceId):
    # generate transaction
    # gateway behavior
    # redirect to gateway
    return redirect(reverse('financeTestGatewayURL'))

def xxxPaymentResponse(request,*args,**kwargs):
    # gateway behavior
    # set result and transaction based result
    res = { 'res' : True, 'invoiceId' : 1, 'context' : '---'}
    return res