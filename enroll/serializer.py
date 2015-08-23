from rest_framework import serializers
from models import enrolledProgramSession,enrolledProgramCourse,enrolledProgram

# ----------------------------------------------------
class enrollProgramCourseSerializer(serializers.ModelSerializer):
    firstname = serializers.ReadOnlyField(source='user.first_name')
    lastname  = serializers.ReadOnlyField(source='user.last_name')
    class Meta:
        model = enrolledProgramCourse
# ----------------------------------------------------
class enrollProgramSessionSerializer(serializers.ModelSerializer):
    firstname = serializers.ReadOnlyField(source='user.first_name')
    lastname  = serializers.ReadOnlyField(source='user.last_name')
    class Meta:
        model = enrolledProgramSession
# ----------------------------------------------------
class enrollProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = enrolledProgram

    def to_representation(self, obj):
        """
        Because enrollProgram is Polymorphic
        """
        if isinstance(obj, enrolledProgramCourse):
            return enrollProgramCourseSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, enrolledProgramSession):
           return enrollProgramSessionSerializer(obj, context=self.context).to_representation(obj)
        return super(enrollProgramSerializer, self).to_representation(obj)
# ----------------------------------------------------
class enrollSessionSerializer(serializers.Serializer):
    club    = serializers.IntegerField()
    week    = serializers.IntegerField()
    cellid  = serializers.IntegerField()
# ----------------------------------------------------