from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from models import agreement
from serializers import agreementSerializer
# ----------------------------------------------------
class agreementList(generics.ListAPIView):
    serializer_class = agreementSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return agreement.objects.active().filter(user = self.request.user)
# ----------------------------------------------------
# ----------------------------------------------------