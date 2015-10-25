from rest_framework import serializers

from models import userCredit
# ----------------------------------------------------
class creditSerializer(serializers.ModelSerializer):
    class Meta:
        model = userCredit
# ----------------------------------------------------