from rest_framework import serializers
from golab.models import *

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'
