from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import BusinessLead
from .serializers import BusinessLeadSerializer

class LeadListView(generics.ListAPIView):
    """
    GET /api/leads/
    Returns a list of all calculated leads, filterable by location or category.
    By default ordered by score descending (as defined in the model Meta).
    """
    queryset = BusinessLead.objects.all()
    serializer_class = BusinessLeadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['has_website', 'category', 'search_request__location', 'search_request__query']
