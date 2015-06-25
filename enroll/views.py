from django.views.generic import ListView, DetailView, View
from django.http import HttpResponseRedirect, HttpResponse

from enroll.models import enrolledProgram

from program.views import userAuthorizeMixin
from program.models import programDefinition

from enroll.enrollcourse.function import enrollCourse
from finance.functions import invoiceGenerate, paymentRequest

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
            enrollInst = enrollCourse(programInst)
            invoiceId = invoiceGenerate(enrollInst)
            return HttpResponse(paymentRequest(invoiceId))
            return HttpResponse('OK')
            return redirect('/')
        else:
            return HttpResponse('ERROR')
            messages.error(request, _('This program is not valid for enroll. Validation expired or no free spcae.'))
            return redirect('directoryItemDetail', slug= programInst.clubSlug())
# ----------------------------------------------------
class enrollmentList(ListView):
    template_name = 'enroll/enrolled_list.html'

    def get_queryset(self):
        return enrolledProgram.objects.filter(user_id = self.request.user.id).\
            filter(status = enrolledProgram.ENROLLMENT_STATUS_PAYED)
# ----------------------------------------------------
class enrollmentList2(userAuthorizeMixin, ListView):
    template_name = 'enroll/enrolled_list.html'
    model = enrolledProgram
    template_name = 'enroll/enrolled_list.html'
    model = enrolledProgram

    def get_queryset(self):
        return enrolledProgram.objects.filter(clubItemDefinitionKey = self.kwargs['programId']).\
            filter(status = enrolledProgram.ENROLLMENT_STATUS_PAYED)
# ----------------------------------------------------
