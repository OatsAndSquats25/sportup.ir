from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from directory.serializers import clubSerializer
from directory.models import club

from models import agreement
from serializers import agreementSerializer
# ----------------------------------------------------
class agreementList(generics.ListAPIView):
    """
    Return active agreement for current user
    """
    serializer_class = agreementSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return agreement.objects.active().filter(user = self.request.user)
# ----------------------------------------------------
class agreementClubs(generics.ListAPIView):
    """
    Return list of clubs with active agreement for current user
    """
    serializer_class = clubSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        agreementInst = agreement.objects.active().filter(user = self.request.user)
        return club.objects.filter(agreement = agreementInst)
        # return club.objects.filter(agreement__user = self.request.user).filter(agreement__isValud = true)

# ----------------------------------------------------