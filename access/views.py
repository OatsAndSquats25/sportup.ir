from rest_framework import generics, views
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
# ----------------------------------------------------
class accessRequest(views.APIView):
# class accessRequest(generics.GenericAPIView):
    """
    Access request for specific user on specific club
    """
    def get(self, request, *args, **kwargs):
        """
        userid      -- user identification
        """
        request.POST.get('userid')
        return Response('not working', status=status.HTTP_204_NO_CONTENT)
# ----------------------------------------------------
class accessRecord(views.APIView):
# class accessRequest(generics.GenericAPIView):
    """
    Access record for specific user enrollment
    """
    def post(self, request, *args, **kwargs):
        """
        enrollid    -- enrollment id for user
        """
        request.POST.get('enrollid')
        return Response('not working', status=status.HTTP_204_NO_CONTENT)
# ----------------------------------------------------
