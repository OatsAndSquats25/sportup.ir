from rest_framework import serializers

from models import access
# ----------------------------------------------------
class accessSerializer(serializers.ModelSerializer):
    class Meta:
        model = access
# ----------------------------------------------------
class accessDirectSerializer(serializers.Serializer):
    enrollid    = serializers.IntegerField()
# ----------------------------------------------------