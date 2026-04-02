from celery import shared_task
from apps.search.models import SearchRequest
from apps.leads.models import BusinessLead
from common.services.search_service import fetch_businesses_from_serp
from common.services.validation_service import check_website_exists
from common.services.scoring_service import calculate_lead_score

@shared_task
def process_search_request(search_id):
    try:
        search_request = SearchRequest.objects.get(id=search_id)
    except SearchRequest.DoesNotExist:
        return
        
    search_request.status = 'PROCESSING'
    search_request.save()
    
    try:
        # 1. Fetch business data using SERP API
        raw_leads = fetch_businesses_from_serp(search_request.query, search_request.location)
        
        leads_to_create = []
        for lead_data in raw_leads:
            # 2. Website Validation
            # If website field is missing or invalid -> mark as potential lead
            website_url = lead_data.get('website')
            has_website = check_website_exists(website_url)
            lead_data['has_website'] = has_website
            
            # 3. Lead Scoring
            score = calculate_lead_score(lead_data)
            
            # Prepare for DB insert
            leads_to_create.append(
                BusinessLead(
                    search_request=search_request,
                    name=lead_data.get('name', '')[:255],
                    category=lead_data.get('category', '')[:255],
                    address=lead_data.get('address', ''),
                    phone=lead_data.get('phone', '')[:50],
                    rating=lead_data.get('rating'),
                    reviews_count=lead_data.get('reviews_count', 0),
                    website=website_url,
                    has_website=has_website,
                    score=score
                )
            )
            
        # 4. Save into BusinessLead model
        if leads_to_create:
            BusinessLead.objects.bulk_create(leads_to_create)
            
        search_request.total_results = len(leads_to_create)
        search_request.status = 'COMPLETED'
        search_request.save()
        
    except Exception as e:
        print(f"Error processing search request {search_id}: {e}")
        search_request.status = 'FAILED'
        search_request.save()
