from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from finance.models import transaction


def paymentRequest(request, InvoiceInst):
    transaction.objects.create(invoiceKey = InvoiceInst,
                           ref_id='111',
                           amount=InvoiceInst.amount,
                           user=request.user)

    return redirect(reverse('financeTestGatewayURL'))

def paymentResponse(request,*args,**kwargs):
    transInst = transaction.objects.get(ref_id='111')
    transInst.trans_id = 'wdlj349cd2143mfd-2'
    transInst.save()

    return{ 'status' : True, 'invoiceId' : transInst.invoiceKey.id }