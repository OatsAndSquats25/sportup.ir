from rest_framework import views, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.utils.timezone import now
from enroll.models import enrolledProgram

from models import access
from serializers import accessSerializer, accessDirectSerializer
# ----------------------------------------------------
# class accessView(views.APIView):
class accessView(generics.GenericAPIView):
    """
    Club access operations
    """
    # serializer_class = accessSerializer
    serializer_class = accessDirectSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        """
        Retrive recorded access for user/specific user
        userid      -- user id (Optional)
        """
        userid = self.request.user
        # userid = self.request.GET.get('userid', self.request.user)
        accessInst = access.objects.filter(user = userid)
        return Response(accessSerializer(accessInst, many=True).data)
    def post(self, request):
        """
        Record access for specific enroll
        """
        #todo  check is this enroll for this club
        # enrollInst = enrolledProgram.objects.get()
        enrollid = request.DATA.get('enrollid','-1')
        if enrollid == '-1':
            return Response("Error", status=status.HTTP_204_NO_CONTENT)
        else:
            enrollInst = enrolledProgram.objects.get(pk=request.DATA.get('enrollid'))
            access.objects.create(enrollKey=enrollInst, user=self.request.user, expiry_date= now())
            return Response("Done")
# ----------------------------------------------------
class accessRequest(views.APIView):
    """
    user access operations
    """
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        """
        userid      -- user id
        """
        # todo check user id and club user to find relevant program for access
        return Response('Access grant',status=status.HTTP_200_OK)
        return Response('Access denid',status=status.HTTP_406_NOT_ACCEPTABLE)
# ----------------------------------------------------
