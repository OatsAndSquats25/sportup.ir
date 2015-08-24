from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from program.models import programDefinition
from finance.functions import invoiceGenerate, paymentRequest

from models import enrolledProgramSession, enrolledProgram
from enrollcourse.function import enrollCourse
from serializer import enrollProgramSerializer,enrollSessionSerializer

from agreement.models import agreement
from programsession.views import sessionGenerateFull
# ----------------------------------------------------
class enrollConfirmation(DetailView):
    """
    Get course confirmation from user
    """
    template_name = 'enroll/enrollment_confirmation.html'
    model = programDefinition
# ----------------------------------------------------
class enrollConfirmed(View):
    """
    Enroll in course and redirect to shopping cart
    """
    def get(self, request, *args, **kwargs):
        programInst = programDefinition.objects.get(pk = kwargs['pk'])
        if programInst.isValid():
            # if programInst.type == :
            enrollInst = enrollCourse(request, programInst)
            return redirect('checkoutURL')
        else:
            messages.error(request, _('This program is not valid for enroll. Validation expired or no free spcae.'))
            return redirect('directoryItemDetail', slug= programInst.clubSlug())
# ----------------------------------------------------
class enrollSessionList(generics.ListAPIView):
    """
    Return list of all enrolled sessions for current user (anyone)
    """
    serializer_class = enrollProgramSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return enrolledProgram.objects.instance_of(enrolledProgramSession).filter(user = user)
        # return enrolledProgram.objects.filter(user = user)
# ----------------------------------------------------
class enrollSessionListClub(generics.ListAPIView):
    """
    Return list of all enrolled sessions for club (club permission)
    agreement -- aggreement id
    """
    serializer_class = enrollProgramSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        agreementInst = agreement.objects.active().filter(user = self.request.user).filter(id=self.request.GET.get('agreement'))
        return enrolledProgramSession.objects.filter(status = enrolledProgramSession.CONTENT_STATUS_ACTIVE).filter(programDefinitionKey__agreementKey = agreementInst).select_related('user')
# ----------------------------------------------------
class enrollSession(generics.GenericAPIView):
    """
    Enroll session related operations
    """
    serializer_class = enrollSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        """
        Retrive enrolled for each session (Club permission)
        club    -- club id
        week    -- select week (current week is 0)
        cellid  -- cellid
        """
        club= int(request.GET.get('club','-1'))
        week= int(request.GET.get('week','-1'))
        id  = int(request.GET.get('cellid','-1'))
        scheduleTable = sessionGenerateFull(club, week)
        cell = filter(lambda x: x.cellid == id, scheduleTable)
        if not cell:
            return Response("No cell exist.",status=status.HTTP_400_BAD_REQUEST)

        enrolledInst = enrolledProgramSession.objects.filter(date = cell[0].date).filter(sessionTimeBegin = cell[0].begin).filter(sessionTimeEnd = cell[0].end)
        return Response(enrollProgramSerializer(enrolledInst, many=True).data)

    def post(self, request, *args, **kwargs):
        """
        Enroll in a specific cell (anyone)
        """
        club= int(request.POST.get('club','-1'))
        week= int(request.POST.get('week','-1'))
        id  = int(request.POST.get('cellid','-1'))

        # if club <= -1 or week <= -1 or id <= -1:
        #     return Response({"detail":"negative value does not allow."})

        scheduleTable = sessionGenerateFull(club, week)
        cell = filter(lambda x: x.cellid == id, scheduleTable)
        if not cell:
            return Response("No cell exist.",status=status.HTTP_400_BAD_REQUEST)
        if cell[0].capacity <= 0:
            return Response("Session does not have enough space.",status=status.HTTP_400_BAD_REQUEST)

        prginst = programDefinition.objects.get(id = cell[0].prgid)
        enrolledProgramSession.objects.create(programDefinitionKey = prginst,
                                              amount = cell[0].price,
                                              date = cell[0].date,
                                              sessionTimeBegin = cell[0].begin,
                                              sessionTimeEnd = cell[0].end,
                                              user = request.user)

        return Response("Done", status=status.HTTP_200_OK)
# ----------------------------------------------------