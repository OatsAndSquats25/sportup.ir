from rest_framework import serializers

from models import agreement
# ----------------------------------------------------
class agreementSerializer(serializers.ModelSerializer):
    clubKey = serializers.StringRelatedField()
    status  = serializers.CharField(source='get_status_display')
    agreementStatus  = serializers.CharField(source='get_agreementStatus_display')

    class Meta:
        model = agreement
# ----------------------------------------------------