from rest_framework import serializers
from models import agreement
# ----------------------------------------------------
class agreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = agreement
# ----------------------------------------------------