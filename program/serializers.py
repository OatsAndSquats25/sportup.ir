from rest_framework import serializers
from models import programDefinition
from programsession.models import sessionDefinition
from programcourse.models import courseDefinition

# ----------------------------------------------------
class courseDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = courseDefinition
# ----------------------------------------------------
class sessionDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = sessionDefinition
# ----------------------------------------------------
class programDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = programDefinition

    def to_representation(self, obj):
        """
        Because programDefinition is Polymorphic
        """
        if isinstance(obj, courseDefinition):
            return courseDefinitionSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, sessionDefinition):
           return sessionDefinitionSerializer(obj, context=self.context).to_representation(obj)
        return super(programDefinitionSerializer, self).to_representation(obj)
# ----------------------------------------------------