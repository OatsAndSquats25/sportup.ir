from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
# ----------------------------------------------------
class accessRequest(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        return Response('not working')

# ----------------------------------------------------
