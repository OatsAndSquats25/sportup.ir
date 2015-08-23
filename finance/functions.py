from django.conf import settings
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum

from models import invoice
from program.models import programDefinition
from enroll.models import enrolledProgram
from finance.models import transaction
from payment import testPay, payline, paylineTest
#----------------------------------------------------------------------
def invoiceGenerate(request):
    """
    Generate invoice for inactive enrollment of current user
    """
    # TODO: check aginst regenerate invoice
    itemsInst = enrolledProgram.objects.filter(user_id = request.user.id).filter(status = enrolledProgram.CONTENT_STATUS_INACTIVE)
    if itemsInst:
        invoiceAmount = itemsInst.aggregate(total = Sum('amount'))['total']
    invoiceInst = invoice.objects.create(amount=invoiceAmount, context=_("Payment pending"), user= request.user)
    enrolledProgram.objects.filter(user_id = request.user.id).filter(status = enrolledProgram.CONTENT_STATUS_INACTIVE).update(invoiceKey = invoiceInst)
    return invoiceInst
#----------------------------------------------------------------------
def invoicePayed(idValue):
    """
    Successful payment of each invoice call this function to update invoice and enroll status
    """
    # change invoice`s status to active
    invoiceInst = invoice.objects.get(pk=idValue)
    invoiceInst.status = enrolledProgram.CONTENT_STATUS_ACTIVE
    invoiceInst.context = _("Payment done")
    invoiceInst.save()

    # change enroll`s status to active
    enrolledInst = enrolledProgram.objects.select_related().filter(invoiceKey = invoiceInst).update(status = enrolledProgram.CONTENT_STATUS_ACTIVE)

    return True
#----------------------------------------------------------------------
def invoiceError(idValue):
    """
    Failed payment of each invoice call this function to update invoice description
    """
    # change invoice`s description to error
    invoiceInst = invoice.objects.get(pk=idValue)
    invoiceInst.context = _("Payment error")
    invoiceInst.save()

    return True
#----------------------------------------------------------------------
def paymentRequest(request, invoiceInst):

    try:
        default_gateway = settings.DEFAULT_PAYMENT_GATEWAY
    except:
        raise Http404

    if default_gateway == 'test':
        return testPay.paymentRequest(request, invoiceInst)
    elif default_gateway == 'payline':
        return payline.paymentRequest(request, invoiceInst)
    elif default_gateway == 'paylinetest':
        return paylineTest.paymentRequest(request, invoiceInst)

#----------------------------------------------------------------------
