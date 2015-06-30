from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from finance.models import transaction

def paymentRequest(request, InvoiceInst):
    # generate transaction
    # gateway behavior
    # redirect to gateway
    transaction.objects.create(invoiceKey = InvoiceInst,
                               ref_id=<<<<id>>>>,
                               amount=InvoiceInst.amount,
                               user=request.user)
    return redirect(<<<<->>>>)

def paymentResponse(request,*args,**kwargs):
    transInst = transaction.objects.get(ref_id=<<<<id>>>>)

    # gateway behavior
    # set result and transaction based result
    #Error
        transInst.description = resCode
        transInst.save()
        return { 'status' : False}
    #Correct
    transInst.trans_id = <<<<trans_id>>>>
    transInst.save()

    return{ 'status' : True, 'invoiceId' : transInst.invoiceKey.id }
