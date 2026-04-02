from rest_framework import generics, status
from rest_framework.response import Response
from apps.leads.models import BusinessLead
from apps.leads.serializers import BusinessLeadSerializer
from .models import SearchRequest
from .serializers import SearchRequestSerializer
from .tasks import process_search_request

class SearchAPIView(generics.CreateAPIView):
    """
    POST /api/search/
    Creates a new SearchRequest and queues the Celery task.
    """
    queryset = SearchRequest.objects.all()
    serializer_class = SearchRequestSerializer

    def perform_create(self, serializer):
        search_request = serializer.save()
        # Trigger background processing
        process_search_request.delay(search_request.id)

class SearchLeadsAPIView(generics.ListAPIView):
    """
    GET /api/search/{id}/leads/
    Returns the generated leads for a specific search request.
    """
    serializer_class = BusinessLeadSerializer

    def get_queryset(self):
        search_id = self.kwargs.get('id')
        return BusinessLead.objects.filter(search_request_id=search_id)
