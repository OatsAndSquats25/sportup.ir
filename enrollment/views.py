from django.views.generic import ListView, DetailView

from enrollment.models import clubItemEnrollment
from program.views import userAuthorizeMixin
from program.models import programDefinition

# ----------------------------------------------------
class enrollmentConfirmation(DetailView):
    template_name = 'enrollment/enrollment_confirmation.html'
    model = programDefinition

# ----------------------------------------------------
class enrollmentList(ListView):
    template_name = 'enrollment/enrolled_list.html'

    def get_queryset(self):
        return clubItemEnrollment.objects.filter(user_id = self.request.user.id).\
            filter(status = clubItemEnrollment.ENROLLMENT_STATUS_PAYED)
# ----------------------------------------------------
class enrollmentList2(userAuthorizeMixin, ListView):
    template_name = 'enrollment/enrolled_list.html'
    model = clubItemEnrollment

    def get_queryset(self):
        return clubItemEnrollment.objects.filter(clubItemDefinitionKey = self.kwargs['programId']).\
            filter(status = clubItemEnrollment.ENROLLMENT_STATUS_PAYED)
# ----------------------------------------------------