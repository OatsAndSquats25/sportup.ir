from rest_framework import serializers

from models import club, imageCollection, address, contact
# ----------------------------------------------------
class clubSerializer(serializers.ModelSerializer):
    class Meta:
        model = club
        # fields =("id", "pk", "title","slug", "status","summary", "detail", "address", "website","phone","cell","logo")
# ---------------------------------------------------
class imageSerializer(serializers.ModelSerializer):
    class Meta:
        model = imageCollection
        fields = ('title','imageFile')
# ---------------------------------------------------
class addressSerializer(serializers.ModelSerializer):
    class Meta:
        model = address
# ---------------------------------------------------
class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact
# ---------------------------------------------------
class clubTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = club
        fields = ('id', 'pk','title')
# ---------------------------------------------------
class clubItemSerializer(serializers.ModelSerializer):
    complexName     = serializers.CharField(source='complex_name')
    complexSummary  = serializers.CharField(source='complex_summary')
    locationName    = serializers.CharField(source='location_name')
    locationAddress = addressSerializer(source='location_address', many=True)
    contacts        = contactSerializer(many=True)
    clubs           = clubTitleSerializer(source='club_related', many=True)
    imageCollection = imageSerializer(many=True)

    class Meta:
        model = club
        # fields =("complexName", "complexSummary", "locationName", "locationAddress", "clubs", "pk", "title","slug", "status","summary", "detail", "address", "website","phone","cell","logo", "imageCollection")
# ---------------------------------------------------
