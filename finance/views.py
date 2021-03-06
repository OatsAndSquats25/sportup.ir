from django.views.generic import TemplateView, ListView, View
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.shortcuts import redirect
from django.http import Http404

from generic import email,sms
from credit.views import userCredit
from enroll.models import enrolledProgram

from payment import testPay,payline,paylineTest,creditpay
from functions import invoicePayed, invoiceError, invoiceGenerate, paymentRequest
# ----------------------------------------------------
class checkout(ListView):
    template_name = 'finance/checkout.html'

    def get_queryset(self):
        return enrolledProgram.objects.filter(user_id = self.request.user.id).filter(status = enrolledProgram.CONTENT_STATUS_INACTIVE).select_related()

    def render_to_response(self, context, **response_kwargs):
        context = super(checkout, self).get_context_data()
        amount = 0

        itemsInst = enrolledProgram.objects.filter(user_id = self.request.user.id).filter(status = enrolledProgram.CONTENT_STATUS_INACTIVE)
        if itemsInst:
            amount = itemsInst.aggregate(total = Sum('amount'))['total']

        context['totalAmount'] = amount

        return super(checkout, self).render_to_response(context)
# ----------------------------------------------------
class checkoutPay(View):
    def post(self,request,*args,**kwargs):
        gateway = self.request.POST.get('gateway','0')

        object_list = enrolledProgram.objects.filter(user_id = self.request.user.id).filter(status = enrolledProgram.CONTENT_STATUS_INACTIVE).select_related()
        if not object_list:
            messages.error(self.request, _("Your shopping cart is empty."))
            return redirect('checkoutURL')

        for object in object_list:
            if not object.isValid():
                messages.error(self.request, _("Please check your cart and remove yellow programs. This programs expired or do not have enough space."))
                return redirect('checkoutURL')

        if gateway == 'creditpay':
            try:
                validCredits = int((userCredit.objects.active().filter(user = request.user).aggregate(overallCredit = Sum('value')))['overallCredit'])
            except:
                validCredits = 0
            remainEnroll = int((enrolledProgram.objects.filter(user_id = self.request.user.id).filter(status = enrolledProgram.CONTENT_STATUS_INACTIVE).aggregate(payable = Sum('amount')))['payable'])

            if remainEnroll > validCredits:
                messages.error(self.request, _("You do not have enough credit to pay your invoice!"))
                return redirect('checkoutURL')

        invoiceInst = invoiceGenerate(self.request)
        return redirect(paymentRequest(self.request, invoiceInst, gateway))

# ----------------------------------------------------
class fianceDeleteItem(View):
    def get(self,request,*args,**kwargs):
        enrolledProgram.objects.get(pk = kwargs['pk']).delete()
        return redirect(request.META['HTTP_REFERER'])
# ----------------------------------------------------
def paymentRes(request, *args, **kwargs):
    gateway = kwargs.pop('gateway')
    if (gateway == 'tst'):
        payRes = testPay.paymentResponse(request,*args,**kwargs)
    elif (gateway == 'pl'):
        payRes = payline.paymentResponse(request,*args,**kwargs)
    elif (gateway == 'plt'):
        payRes = paylineTest.paymentResponse(request,*args,**kwargs)
    else:
        messages.error(request, _("We do not support this payment gateway"))
        raise Http404

    if payRes['status'] == True :
        invoicePayed(request, payRes['invoiceId'])
        messages.success(request, _("Payment was successful."))
        return reverse('paymentSucceededURL')
    else:
        invoiceError(payRes['invoiceId'])
        messages.error(request, _("Payment has error"))
        return reverse('paymentFailedURL')
# ----------------------------------------------------
class paymentResponse(View):
    def get(self,request,*args,**kwargs):
        return redirect(paymentRes(request, *args, **kwargs))
    def post(self,request,*args,**kwargs):
        return redirect(paymentRes(request, *args, **kwargs))
# ----------------------------------------------------
class testGateway(TemplateView):
    template_name = 'finance/testgateway.html'
# ----------------------------------------------------
# class financeHistory(ListView):
#     model = models.accountingBook
#     # show last 20 transaction
# ----------------------------------------------------
# class financeDefray(ListView):
#     model = models.accountingBook
#     # show account eligible for defray but not dfray
#     # capability for defray and insert finance document
# ----------------------------------------------------
class paymentSucceeded(TemplateView):
    template_name = 'finance/paymentSucceeded.html'
    #def get_context_data(self, **kwargs):
    #    context = {'nextPage': kwargs.get("next")}
    #    return context

# -----------------------------------------------------------------------
class paymentFailed(TemplateView):
    template_name = 'finance/paymentFailed.html'
    #def get_context_data(self, **kwargs):
    #    context = {'nextPage': kwargs.get("next")}
    #    return context

# -----------------------------------------------------------------------