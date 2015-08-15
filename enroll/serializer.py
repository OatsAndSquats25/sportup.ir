from rest_framework import serializers
from models import enrolledProgramSession


class enrolledProgramSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = enrolledProgramSession

class enrolledProgramSessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = enrolledProgramSession
        fields = ('programDefinitionKey', 'date', 'sessionTimeBegin', 'sessionTimeEnd',)