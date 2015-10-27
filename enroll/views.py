from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from accounts.models import userProfile
from program.models import programDefinition
from finance.functions import invoiceGenerate, paymentRequest

from models import enrolledProgramSession, enrolledProgram, enrolledProgramCourse
from programcourse.models import courseDefinition
from enrollcourse.function import enrollCourseFunction
from enrollsession.function import enrollSessionFunction
from serializer import enrollProgramSerializer,enrollSessionSerializer, enrollSessionClubSerializer, enrollCourseClubSerializer

from agreement.models import agreement
from programsession.views import sessionGenerateFull
from generic import email

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
            #enrollInst = enrollCourse(request, programInst) #:commented by ali since it has an error (could not find enroll course)
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

    def get(self, request, *args, **kwargs):
        """
        Return list of all enrolled sessions for club (club permission)
        clubid -- club id
        """
        enrollInst = enrolledProgramSession.objects.filter(status = enrolledProgramSession.CONTENT_STATUS_ACTIVE).filter(programDefinitionKey__clubKey = self.request.GET.get('clubid')).filter(date = now().date()).select_related('user').order_by("firstAccess", "sessionTimeBegin")
        return Response(enrollProgramSerializer(enrollInst, many=True).data)

    def post(self, request, *args, **kwargs):
        """
        Enroll in a specific cell (anyone)
        """
        _club    = int(request.data.get('club','-1'))
        _week    = int(request.data.get('week','-1'))
        _cellid  = int(request.data.get('cellid','-1'))
        _first   = request.data.get('firstName', '')
        _last    = request.data.get('lastName', '')
        _email   = request.data.get('eMail', '')
        _cellP   = request.data.get('cellPhone','')
        _desc    = _first + ' ' + _last + "-" + _cellP

        if _club == -1 or _week == -1 or _cellid == -1 or _first == '' or _last == '':
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
                userInst = UserModel.objects.create_user(UserModel.objects.count()+1, email = _email, first_name = _first, last_name = _last)
                userProfile.objects.create(user = userInst, cellPhone = _cellP)
                #send_approved_mail(request, userInst)
                # todo est cellphone number
            _user = userInst
        else:
            _user = self.request.user
            pass

        prginst = programDefinition.objects.get(id = cell[0].prgid)
        enrollInst = enrolledProgramSession.objects.create(programDefinitionKey = prginst,
                                              amount = cell[0].price,
                                              date = cell[0].date,
                                              sessionTimeBegin = cell[0].begin,
                                              sessionTimeEnd = cell[0].end,
                                              user = _user,
                                              status = programDefinition.CONTENT_STATUS_ACTIVE,
                                              title= _desc)
        if _email :
            email.reservedByClub(request, request.user, enrollInst.programDefinitionKey.clubKey, _email)
        return Response(enrollInst.id, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        _id = kwargs.get("pk", "-1")
        try:
            enrollInst = enrolledProgramSession.objects.filter(id = _id).filter(user = request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response("you can not delete this user.",status=status.HTTP_404_NOT_FOUND)
            #return super(enrollSessionClub, self).destroy(request,args, kwargs)
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
        _club    = int(request.data.get('club','-1'))
        _week    = int(request.data.get('week','-1'))
        _cellid  = int(request.data.get('cellid','-1'))

        if _club == -1 or _week == -1 or _cellid == -1:
            return Response('Input parameters are not valid !',status=status.HTTP_400_BAD_REQUEST)

        scheduleTable = sessionGenerateFull(_club, _week)
        cell = filter(lambda x: x.cellid == _cellid, scheduleTable)
        if not cell:
            return Response("No cell exist.",status=status.HTTP_400_BAD_REQUEST)
        if cell[0].capacity <= 0:
            return Response("Session does not have enough space.",status=status.HTTP_400_BAD_REQUEST)
        _desc    = request.user.get_full_name()
        prginst = programDefinition.objects.get(id = cell[0].prgid)
        enrollInst = enrolledProgramSession.objects.create(programDefinitionKey = prginst,
                                              amount = cell[0].price,
                                              date = cell[0].date,
                                              sessionTimeBegin = cell[0].begin,
                                              sessionTimeEnd = cell[0].end,
                                              user = self.request.user,
                                              title = _desc)

        return Response("Done", status=status.HTTP_200_OK)
# ----------------------------------------------------
class enrollInCourse(View):
    """
    Enroll in course and redirect to shopping cart
    """
    def post(self, request, *args, **kwargs):
        if enrollCourseFunction(request):
            return redirect('checkoutURL')
        else:
            messages.error(request, _('This program is not valid for enroll. Validation expired or no free spcae.'))
            return redirect(request.META.get('HTTP_REFERER'))
# ----------------------------------------------------
class enrollInSession(View):
    """
    Enroll in session and redirect to shopping cart
    """
    def post(self, request, *args, **kwargs):
        if enrollSessionFunction(request):
            return redirect('checkoutURL')
        else:
            messages.error(request, _('This program is not valid for enroll. Validation expired or no free spcae.'))
            return redirect(request.META.get('HTTP_REFERER'))
# ----------------------------------------------------
class enrollCourseClub(generics.GenericAPIView):
    """
    enroll session club
    """
    serializer_class = enrollCourseClubSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Return list of all enrolled sessions for club (club permission)
        clubId -- club id
        courseId -- course id
         """
        enrollInst = enrolledProgramCourse.objects.filter(status = enrolledProgramSession.CONTENT_STATUS_ACTIVE).filter(programDefinitionKey__id = self.request.GET.get('courseId')).select_related('user')
        return Response(enrollProgramSerializer(enrollInst, many=True).data)

    def post(self, request, *args, **kwargs):
        """
        Enroll in a specific cell (anyone)
        """
        _course  = int(request.data.get('courseId', '-1'))
        _first   = request.data.get('firstName', '')
        _last    = request.data.get('lastName', '')
        _email   = request.data.get('eMail', '')
        _cellP   = request.data.get('cellPhone','')
        _desc    = _first + ' ' + _last + "-" + _cellP

        if _course == -1 or _first == '' or _last == '':
            return Response('Input parameters are not valid !',status=status.HTTP_400_BAD_REQUEST)

        courseInst = courseDefinition.objects.get(id = _course)
        if courseInst.remainCapacity <= 0:
            return Response("Session does not have enough space.",status=status.HTTP_400_BAD_REQUEST)
        courseInst.remainCapacity -= 1
        courseInst.save()
        # email provide: user exist: enroll for user
        # email provide: user not exist: create user and enroll for user
        # email not provide: enroll with current user, add information to title
        if _email:
            UserModel = get_user_model()
            try:
                userInst = UserModel.objects.get(email = _email)
            except UserModel.DoesNotExist:
                userInst = UserModel.objects.create_user(UserModel.objects.count()+1, email = _email, first_name = _first, last_name = _last)
                userProfile.objects.create(user = userInst, cellPhone = _cellP)
                #send_approved_mail(request, userInst)
                # todo est cellphone number
            _user = userInst
        else:
            _user = self.request.user
            pass

        enrollInst = enrolledProgramCourse.objects.create(programDefinitionKey = courseInst,
                                              amount = courseInst.price,
                                              user = _user,
                                              status = programDefinition.CONTENT_STATUS_ACTIVE,
                                              title= _desc)
        if _email :
            email.reservedByClub(request, request.user, enrollInst.programDefinitionKey.clubKey, _email)
        return Response(enrollInst.id, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        _id = kwargs.get("pk", "-1")
        try:
            enrollInst = enrolledProgramCourse.objects.filter(id = _id).filter(user = request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response("you can not delete this user.",status=status.HTTP_404_NOT_FOUND)