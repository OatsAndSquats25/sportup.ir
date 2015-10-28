from django.conf import settings
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum

from generic import email,sms
from models import invoice
from credit.models import userCredit
from program.models import programDefinition
from enroll.models import enrolledProgram
from finance.models import transaction
from payment import testPay, payline, paylineTest, creditpay
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
def invoicePayed(request, idValue):
    """
    Successful payment of each invoice call this function to update invoice and enroll status
    """
    # change invoice`s status to active
    invoiceInst = invoice.objects.get(pk=idValue)
    invoiceInst.status = enrolledProgram.CONTENT_STATUS_ACTIVE
    invoiceInst.context = _("Payment done")
    invoiceInst.save()

    # change enroll`s status to active
    # enrolledInst = enrolledProgram.objects.select_related().filter(invoiceKey = invoiceInst).update(status = enrolledProgram.CONTENT_STATUS_ACTIVE)

    enrolledInst = enrolledProgram.objects.select_related().filter(invoiceKey = invoiceInst).update(status = enrolledProgram.CONTENT_STATUS_ACTIVE)
    creditInst = userCredit.objects.select_related().filter(invoiceKey = invoiceInst).update(status = enrolledProgram.CONTENT_STATUS_ACTIVE)

    if enrolledInst:
        sms.reservedByAthlete(request, invoiceInst)
        email.reservedByAthlete(request, request.user, invoiceInst)

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
def paymentRequest(request, invoiceInst, _gateway='0'):

    try:
        if _gateway == '0':
            default_gateway = settings.DEFAULT_PAYMENT_GATEWAY
        else:
            default_gateway = _gateway
    except:
        raise Http404

    if default_gateway == 'test':
        return testPay.paymentRequest(request, invoiceInst)
    elif default_gateway == 'payline':
        return payline.paymentRequest(request, invoiceInst)
    elif default_gateway == 'paylinetest':
        return paylineTest.paymentRequest(request, invoiceInst)
    elif default_gateway == 'creditpay':
        returnAddress = creditpay.paymentRequest(request, invoiceInst)
        invoicePayed(request, invoiceInst.id)
        return returnAddress

#----------------------------------------------------------------------
