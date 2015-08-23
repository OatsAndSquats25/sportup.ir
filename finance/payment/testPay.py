from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from finance.models import transaction


def paymentRequest(request, InvoiceInst):
    transaction.objects.create(invoiceKey = InvoiceInst,
                           ref_id=str(InvoiceInst.id) + '11',
                           amount=InvoiceInst.amount,
                           user=request.user)

    return reverse('financeTestGatewayURL', kwargs={'refid':str(InvoiceInst.id) + '11'})

def paymentResponse(request,*args,**kwargs):
    transInst = transaction.objects.get(ref_id = request.GET.get('refid'))

    if request.GET.get('trans') == '-1':
        transInst.description = 'Failed'
    else:
        transInst.description = 'success'
        transInst.trans_id = request.GET.get('trans')
    transInst.save()

    if request.GET.get('trans') == '-1':
        return{ 'status' : False, 'invoiceId' : transInst.invoiceKey.id }
    else:
        return{ 'status' : True, 'invoiceId' : transInst.invoiceKey.id }