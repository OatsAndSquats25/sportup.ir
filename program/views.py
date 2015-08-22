from rest_framework import generics
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from models import programDefinition
from serializers import programDefinitionSerializer
# ----------------------------------------------------
class programInformation(generics.RetrieveAPIView):
    """
    Return program information
    """
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = programDefinition.objects.all()
    serializer_class = programDefinitionSerializer
# ----------------------------------------------------
