from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse

from generic.models import CONTENT_STATUS_ACTIVE
from program.models import programDefinition
# Create your views here.

class programPaymentReq(View):
    def get(self, request, *args, **kwargs):
        # check
        programInst = programDefinition.objects.get(pk = kwargs['pk'])
        if programInst.isValid() :
            #redirect to Bank
            return HttpResponse('OK')
            return redirect('/')
        else:
            return HttpResponse('ERROR')
            messages.error(request, _('This program is not valid for enroll. Validation expired or no free spcae.'))
            return redirect('directoryItemDetail', slug= programInst.clubSlug())