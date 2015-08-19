from rest_framework import serializers
from models import enrolledProgramSession,enrolledProgramCourse,enrolledProgram

# ----------------------------------------------------
class enrollCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = enrolledProgramCourse
# ----------------------------------------------------
class enrollSessionSerializer(serializers.ModelSerializer):
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
            return enrollCourseSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, enrolledProgramSession):
           return enrollSessionSerializer(obj, context=self.context).to_representation(obj)
        return super(enrollProgramSerializer, self).to_representation(obj)
# ----------------------------------------------------