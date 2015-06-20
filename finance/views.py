from django.views.generic import TemplateView, ListView, View
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Sum,F

from mezzanine.core import models as mezModels
from enrollment.models import clubItemEnrollment, clubItemDefinition

from .payment import testBank,saman
from finance import models
from finance import utils

# ----------------------------------------------------
class financeOrder(ListView):
    template_name = 'finance/order.html'

    def get_queryset(self):
        return clubItemEnrollment.objects.filter(user_id = self.request.user.id).filter(status = clubItemEnrollment.ENROLLMENT_STATUS_RESERVED)

    def get_context_data(self, **kwargs):
        context = super(financeOrder, self).get_context_data()

        amount = 0
        discount = 0

        itemsInst = clubItemEnrollment.objects.filter(user_id = self.request.user.id).filter(status = clubItemEnrollment.ENROLLMENT_STATUS_RESERVED)
        if itemsInst:
            amount = itemsInst.aggregate(total = Sum('amount'))['total']

        #if discountInst:
        #    discount = 0

        context['totalAmount'] = amount
        context['discount'] = discount
        context['payable'] = amount - discount

        return context
# ----------------------------------------------------
class fianceDeleteItem(View):
    def get(self,request,*args,**kwargs):
        models.clubItemEnrollment.objects.get(pk = kwargs['pk']).delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
# ----------------------------------------------------
class paymentRequest(TemplateView):
    template_name = 'finance/payment_request.html'

    def post(self,request,*args,**kwargs):
        context = self.get_context_data()

        payable = float(request.POST.get('payable'))
        count = int(request.POST.get('count'))
        gatewayName = request.POST.get('paymentGateway')

        if payable <= 0 :
            messages.error(request,_("There is no payable cost."))
            return HttpResponseRedirect(reverse('financeOrderURL'))

        dataSetPK = []
        for i in range(1,count+1):
            dataSetPK += [int(request.POST.get(str(i))),]

        clubEnInst = clubItemEnrollment.objects.select_related().filter(pk__in = dataSetPK)
        # check all items are valid

        for item in clubEnInst:
            if not item.clubItemDefinitionKey.isValid():
                messages.error(request, _("There are some invalid enrollment in you order please remove them. Maybe it is full or expired."))
                return HttpResponseRedirect(reverse('financeOrderURL'))

        # remove incomplete old invoices
            invoiceInst= models.invoice.objects.filter(paid = False).filter(user_id = request.user.id)
            if invoiceInst:
                for invItem in invoiceInst:
                    clubItemEnrollment.objects.filter(invoiceKey=invItem).update(invoiceKey = 0)
                invoiceInst.delete()

        #utils.clearUnusedReservedItems(self.request)

        # create invoice
        invoiceInst = models.invoice.objects.create(title = _("Invoice"),
                                                    amount = payable,
                                                    user_id = request.user.id,
                                                    status = mezModels.CONTENT_STATUS_DRAFT,
                                                    content='None')
        # connect invoice to related items
        clubItemEnrollment.objects.select_related().filter(pk__in = dataSetPK).update(invoiceKey = invoiceInst)

        # Call specific payment request with reserve number and amount
        if gatewayName == 'test':
            paymentGateway = testBank.Payment()
        elif gatewayName == 'saman':
            paymentGateway = saman.Payment()

        context['payment'] = paymentGateway.sendGatewayRequest(request, invoiceInst.id, payable)

        return self.render_to_response(context)
 # ----------------------------------------------------
class paymentResponse(View):

    def post(self,request,*args,**kwargs):
        #Check for correct response and detect fake or hacker generated
        # Dispatch and call specific payment response
        paymentGateway = testBank.Payment()
        # function return values(Transaction Stat, Reference number, Reserve number)
        gatewayResult = paymentGateway.receiveGatewayResponse(self.request)

        transactionString = 'Error'
        transactionST = gatewayResult['TransactionState']

        try:
            invoiceInst = models.invoice.objects.get(pk=gatewayResult['ReservationNumber'])
        except:
            # TODO: we must record this payment for conflict
            models.accountingBook.objects.create(debit=0,
                                    transaction=transactionST,
                                    transactionStatus=transactionST,
                                    content='ERROR: Invoice doesn`t exist',
                                    user_id = self.request.user.id)

            raise Http404()

        if invoiceInst.paid:
            models.accountingBook.objects.create(invoiceKey=invoiceInst,
                                                debit=0,
                                                transaction=transactionST,
                                                transactionStatus=transactionST,
                                                content='ERROR: Double payment on this invoice',
                                                user_id = self.request.user.id)
            raise Http404()

        if transactionST == 'OK':
            # record transaction success for invoice (Debtor)
            transactionString = gatewayResult['ReferenceNumber']
            # record invoice (Debtor)
            models.accountingBook.objects.create(invoiceKey=invoiceInst,
                                                 debit = invoiceInst.amount,
                                                 transaction = transactionString,
                                                 transactionStatus=transactionST,
                                                 content='None',
                                                 user_id = self.request.user.id)
            # record invoice (Creditor)
            models.accountingBook.objects.create(invoiceKey=invoiceInst,
                                                 credit = invoiceInst.amount,
                                                 content='None',
                                                 user_id = self.request.user.id)
            # update invoice status
            invoiceInst.paid = True
            invoiceInst.status = mezModels.CONTENT_STATUS_PUBLISHED
            invoiceInst.save()

            # record financial documents for company and club
            clubEnInst = clubItemEnrollment.objects.filter(invoiceKey = invoiceInst).select_related()
            for item in clubEnInst:
                agreement = item.clubItemDefinitionKey.agreementKey
                commission = item.clubItemDefinitionKey.agreementKey.commission
                companyAmount= item.amount * commission
                clubAmount= item.amount - companyAmount

                # record financial company (Debtor)
                models.accountingBook.objects.create(invoiceKey=item.invoiceKey,
                                                     agreementKey=agreement,
                                                     enrollmentKey=item,
                                                     debit =companyAmount ,
                                                     company =True,
                                                     content='None',
                                                     user_id = self.request.user.id)
                # record financial club (Debtor)
                models.accountingBook.objects.create(invoiceKey=item.invoiceKey,
                                                     agreementKey=agreement,
                                                     enrollmentKey=item,
                                                     debit=clubAmount,
                                                     defray= models.accountingBook.DEFRAY_NO,
                                                     content='None',
                                                     user_id = self.request.user.id)
                item.status = item.ENROLLMENT_STATUS_PAYED
                #item.clubItemDefinitionKey.remainCapacity -= 1
                item.save()

            #clubItemDefinition.objects.filter(clubItemEnrollment__).update(remainCapacity = F('remainCapacity')-1)
            # reduce enrollment capacity here or at enrollment
            #clubDef = clubItemDefinition.objects.filter()
            #clubDef.reservedCapacity -= 1
            #clubDef.save()
            messages.success(request, _("Payment was successful."))
            return HttpResponseRedirect(reverse('financeOrderURL'))
        else :
            # record transaction not successful (Debtor)
            inst = models.accountingBook.objects.create(debit=0,
                                                        transaction=transactionString,
                                                        transactionStatus=transactionST,
                                                        content='None',
                                                        user_id = self.request.user.id)
            # Remove invoice
            clubItemEnrollment.objects.filter(invoiceKey = invoiceInst).update(invoiceKey = 0)

            invoiceInst.delete()
            #invoiceInst.save()
            ## Variables: reserve, reference, state
            messages.error(request, _("Payment was not successful."))
            return HttpResponseRedirect(reverse('financeOrderURL'))
# ----------------------------------------------------
class financeHistory(ListView):
    model = models.accountingBook
    # show last 20 transaction
# ----------------------------------------------------
class financeDefray(ListView):
    model = models.accountingBook
    # show account eligible for defray but not dfray
    # capability for defray and insert finance document
# ----------------------------------------------------