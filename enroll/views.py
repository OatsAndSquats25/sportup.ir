from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from accounts.models import userProfile
from program.models import programDefinition
from finance.functions import invoiceGenerate, paymentRequest

from models import enrolledProgramSession, enrolledProgram
from enrollcourse.function import enrollCourse
from serializer import enrollProgramSerializer,enrollSessionSerializer, enrollSessionClubSerializer

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
class enrollSessionUser(generics.ListAPIView):
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
class enrollSessionClub(generics.GenericAPIView):
    """
    enroll session club
    """
    serializer_class = enrollSessionClubSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Return list of all enrolled sessions for club (club permission)
        clubid -- club id
        """
        enrollInst = enrolledProgramSession.objects.filter(status = enrolledProgramSession.CONTENT_STATUS_ACTIVE).filter(programDefinitionKey__clubKey = self.request.GET.get('clubid')).select_related('user')
        return Response(enrollProgramSerializer(enrollInst, many=True).data)

    def post(self, request, *args, **kwargs):
        """
        Enroll in a specific cell (anyone)
        """
        _club    = int(request.DATA.get('club','-1'))
        _week    = int(request.DATA.get('week','-1'))
        _cellid  = int(request.DATA.get('cellid','-1'))
        _first   = request.DATA.get('firstName', '')
        _last    = request.DATA.get('lastName', '')
        _email   = request.DATA.get('eMail', '')
        _cellP   = request.DATA.get('cellPhone','')
        _desc    = ''

        if _club == -1 or _week == -1 or _cellid == -1 or _first == None or _last == None:
            return Response('Input parameters are not valid !',status=status.HTTP_400_BAD_REQUEST)

        scheduleTable = sessionGenerateFull(_club, _week)
        cell = filter(lambda x: x.cellid == _cellid, scheduleTable)
        if not cell:
            return Response("No cell exist.",status=status.HTTP_400_BAD_REQUEST)
        if cell[0].capacity <= 0:
            return Response("Session does not have enough space.",status=status.HTTP_400_BAD_REQUEST)

        # email provide: user exist: enroll for user
        # email provide: user not exist: create user and enroll for user
        # email not provide: enroll with current user, add information to title
        if _email:
            UserModel   = get_user_model()
            try:
                userInst = UserModel.objects.get(email = _email)
            except UserModel.DoesNotExist:
                userInst = UserModel.objects.create_user(UserModel.objects.count(), email = _email, first_name = _first, last_name = _last)
                userProfile.objects.create(user = userInst, cellPhone = _cellP)
                # todo est cellphone number
            _user = userInst
        else:
            _user = self.request.user
            _desc = _first + ' ' + _last + "-" + _cellP
            pass

        prginst = programDefinition.objects.get(id = cell[0].prgid)
        enrolledProgramSession.objects.create(programDefinitionKey = prginst,
                                              amount = cell[0].price,
                                              date = cell[0].date,
                                              sessionTimeBegin = cell[0].begin,
                                              sessionTimeEnd = cell[0].end,
                                              user = _user,
                                              status = programDefinition.CONTENT_STATUS_ACTIVE,
                                              title= _desc)

        return Response("Done", status=status.HTTP_200_OK)
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
        _club    = int(request.DATA.get('club','-1'))
        _week    = int(request.DATA.get('week','-1'))
        _cellid  = int(request.DATA.get('cellid','-1'))

        if _club == -1 or _week == -1 or _cellid == -1:
            return Response('Input parameters are not valid !',status=status.HTTP_400_BAD_REQUEST)

        scheduleTable = sessionGenerateFull(_club, _week)
        cell = filter(lambda x: x.cellid == _cellid, scheduleTable)
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
                                              user = self.request.user)

        return Response("Done", status=status.HTTP_200_OK)
# ----------------------------------------------------