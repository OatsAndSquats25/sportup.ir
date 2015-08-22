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
from generic.models import Displayable
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
class enrollSessionList(generics.ListAPIView):
    """
    Return list of all enrolled sessions for current user
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
    Return list of all enrolled sessions for club
    """
    serializer_class = enrollProgramSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # user = self.request.user
        agreementInst = agreement.objects.active().filter(user = self.request.user).filter(id=self.kwargs['agreement'])
        return enrolledProgramSession.objects.filter(status = Displayable.CONTENT_STATUS_ACTIVE).filter(programDefinitionKey__agreementKey = agreementInst)
# ----------------------------------------------------
class enrollSession(generics.GenericAPIView):
    """
    Enroll single session for current user
    """
    serializer_class = enrollSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        club= int(kwargs.get('club','-1'))
        week= int(kwargs.get('week','-1'))
        id  = int(kwargs.get('id','-1'))

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

        # return Response('Done')
        from programsession.serializers import cellSerializer
        return Response(cellSerializer(cell[0]).data)
# ----------------------------------------------------