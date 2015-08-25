from rest_framework import serializers

from models import club
# ----------------------------------------------------
class clubSerializer(serializers.ModelSerializer):
    class Meta:
        model = club
# ----------------------------------------------------