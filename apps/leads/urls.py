from django.urls import path
from .views import LeadListView

urlpatterns = [
    path('leads/', LeadListView.as_view(), name='lead-list'),
]
