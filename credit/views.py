from django.contrib import messages
from django.views.generic import FormView
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.db import models
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta

from models import userCredit
from forms import creditForm
# ----------------------------------------------------

#def add_comment(request):
#	if request.method == "POST":
#		f = creditForm(request.POST)
#		if f.is_valid():
#			c = f.save(commit=False)
#			c.publish_date = datetime.now()
#			c.expiry_date = models.DateTimeField(default=datetime.now()+timedelta(days=30))
#			c.save()
#		return HttpResponseRedirect('/')
#	else:
#		f = creditForm()
#	args = {}
#	args.update(csrf(request))
#	args['form'] = f
#	return render_to_response("credit/credit.html", args)


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

def paymentWithCredit(self, request, **kwargs):
    amount = kwargs.get("amount")
    validCredits = userCredit.objects.filter(user = self.request.user).active()
    validCreditsSum = sum(validCredits, 0)

    if validCreditsSum.overallCredit >= amount:
        for credit in validCredits:
            if amount == 0:
                break
            else:
                if credit.value > amount:
                    credit.value -= amount
                    amount = 0
                else:
                    credit.value = 0
                    amount -= credit.value
                credit.save()
        return True
    else:
        return False
