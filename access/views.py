from rest_framework import generics, views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
# ----------------------------------------------------
class accessRequest(views.APIView):
# class accessRequest(generics.GenericAPIView):
    """
    Request access for specific user to specific club
    """
    def get(self, request, *args, **kwargs):
        return Response('not working')
# ----------------------------------------------------
class accessRecord(views.APIView):
# class accessRequest(generics.GenericAPIView):
    """
    Record access for specific enrollment
    """
    def post(self, request, *args, **kwargs):
        return Response('not working')
# ----------------------------------------------------
