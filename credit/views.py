from django.contrib import messages
from django.views.generic import FormView
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from models import userCredit
from forms import creditForm
# ----------------------------------------------------
class addCredit(FormView):
    """
    Adding credit for current user
    """
    form_class = creditForm
    template_name = "credit/credit.html"
    success_url = "/"
    def form_valid(self, form):
        messages.info(self.request,_("credit has been successfully added."))
        return super(addCredit, self).form_valid(form)

# ----------------------------------------------------

def paymentWithCredit(self, request):
    amount = 10
    validCredits = userCredit.objects.filter(user = self.request.user).active()
    validCreditsSum = sum(validCredits, 0)

    if validCreditsSum.overallCredit >= amount:
        for credit in validCredits:
            if amount == 0:
                break
            else:
                newCreditInst = userCredit(user = credit.user, value = -credit.value if amount > credit.value else -amount)
                amount -= newCreditInst.value
                newCreditInst.save()
    else:
        return
