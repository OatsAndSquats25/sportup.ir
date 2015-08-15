from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated

from program.models import programDefinition
from finance.functions import invoiceGenerate, paymentRequest

from models import enrolledProgramSession
from enrollcourse.function import enrollCourse
from serializer import enrolledProgramSessionSerializer,enrolledProgramSessionCreateSerializer


# ----------------------------------------------------
class enrollConfirmation(DetailView):
    template_name = 'enroll/enrollment_confirmation.html'
    model = programDefinition

# ----------------------------------------------------
class enrollConfirmed(View):
    def get(self, request, *args, **kwargs):
        programInst = programDefinition.objects.get(pk = kwargs['pk'])
        if programInst.isValid():
            # if programInst.type == :
            enrollInst = enrollCourse(request, programInst)
            invoiceInst = invoiceGenerate(request, enrollInst)
            return paymentRequest(request, invoiceInst)
        else:
            messages.error(request, _('This program is not valid for enroll. Validation expired or no free spcae.'))
            return redirect('directoryItemDetail', slug= programInst.clubSlug())
# ----------------------------------------------------
class enrollSessionList(ListAPIView):
    serializer_class = enrolledProgramSessionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return enrolledProgramSession.objects.filter(user = user)
# ----------------------------------------------------
class enrollSessionCreate(CreateAPIView):
    serializer_class = enrolledProgramSessionCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # validate session for enough space and layout activation #fixme
        serializer.save(user=self.request.user, amount = '10') #fixme
# ----------------------------------------------------