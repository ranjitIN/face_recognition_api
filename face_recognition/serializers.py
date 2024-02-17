from rest_framework import serializers
from .models import Person,PersonFaceImage

class PersonSerialzers(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class PersonFaceImageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = PersonFaceImage
        fields = '__all__'