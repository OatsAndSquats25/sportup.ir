from rest_framework import serializers

from models import club, imageCollection, complexLocation
# ----------------------------------------------------
class clubSerializer(serializers.ModelSerializer):
    class Meta:
        model = club
        fields =("pk", "title","slug", "status","summary", "detail", "address", "website","phone","cell","logo")
# ---------------------------------------------------
class imageSerializer(serializers.ModelSerializer):
    class Meta:
        model = imageCollection
        fields = ('title','imageFile')
# ---------------------------------------------------
# class locationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = complexLocation
#         fields = ()
# ---------------------------------------------------
class clubItemSerializer(serializers.ModelSerializer):
    complexName = serializers.CharField(source='complex_name')
    locationName = serializers.CharField(source='location_name')
    imageCollection = imageSerializer(many=True)
    # imageCollection = serializers.StringRelatedField(many=True)

    class Meta:
        model = club
        fields =("complexName", "locationName", "pk", "title","slug", "status","summary", "detail", "address", "website","phone","cell","logo", "imageCollection")
# ---------------------------------------------------
