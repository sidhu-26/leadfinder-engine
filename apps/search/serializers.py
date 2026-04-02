from rest_framework import serializers
from .models import SearchRequest

class SearchRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchRequest
        fields = '__all__'
        read_only_fields = ['status', 'total_results']
