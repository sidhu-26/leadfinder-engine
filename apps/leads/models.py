from django.db import models
from apps.search.models import SearchRequest

class BusinessLead(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    reviews_count = models.IntegerField(default=0)
    website = models.URLField(blank=True, null=True)
    has_website = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    search_request = models.ForeignKey(SearchRequest, on_delete=models.SET_NULL, null=True, related_name='leads')

    class Meta:
        db_table = 'business_leads'
        ordering = ['-score', '-created_at']

    def __str__(self):
        return f"{self.name} - Score: {self.score}"
