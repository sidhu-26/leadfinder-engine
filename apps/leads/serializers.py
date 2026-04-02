from rest_framework import serializers
from .models import BusinessLead

class BusinessLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessLead
        fields = '__all__'
