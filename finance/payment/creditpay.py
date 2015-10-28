from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib import messages


from credit.models import userCredit
from finance.models import transaction
#---------------------------------------------------------------------------------------
def paymentRequest(request, InvoiceInst):

    amount = InvoiceInst.amount
    validCredits = userCredit.objects.active().filter(user = request.user).order_by("expiry_date")
    for credit in validCredits:
        if credit.value >= amount:
            credit.value -= amount
            amount = 0
        else:
            amount -= credit.value
            credit.value = 0
        credit.save()

    transaction.objects.create(invoiceKey = InvoiceInst,
                               ref_id='credit',
                               amount=InvoiceInst.amount,
                               user=request.user)

    messages.info(request, _("Your payment has been done by your credit."))
    return reverse('checkoutURL')
#---------------------------------------------------------------------------------------
def paymentResponse(request):
    pass
    # return{ 'status' : True, 'invoiceId' : transInst.invoiceKey.id }
#---------------------------------------------------------------------------------------