from django.urls import path
from .views import SearchAPIView, SearchLeadsAPIView

urlpatterns = [
    path('search/', SearchAPIView.as_view(), name='search-create'),
    path('search/<int:id>/leads/', SearchLeadsAPIView.as_view(), name='search-leads-list'),
]
