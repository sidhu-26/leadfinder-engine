import requests
from django.conf import settings

def fetch_businesses_from_serp(query: str, location: str) -> list:
    """
    Fetches business leads using a SERP API provider.
    For this example we use standard SERP API format like SerpApi Google Local.
    """
    api_key = settings.SERP_API_KEY
    # Simulate API URL
    url = "https://serpapi.com/search.json"
    
    params = {
        "engine": "google_local",
        "q": query,
        "location": location,
        "api_key": api_key,
    }
    
    # Mocking response for local development if the mock_key is used
    if api_key == 'mock_serp_api_key_123':
        return _get_mocked_results(query, location)
        
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("local_results", [])
        return _format_results(results)
    except requests.RequestException as e:
        print(f"Error fetching from SERP API: {e}")
        return []

def _format_results(results_list: list) -> list:
    formatted_leads = []
    for item in results_list:
        formatted_leads.append({
            "name": item.get("title", ""),
            "category": item.get("type", ""),
            "address": item.get("address", ""),
            "phone": item.get("phone", ""),
            "rating": item.get("rating", 0.0),
            "reviews_count": item.get("reviews", 0),
            "website": item.get("website", ""),
        })
    return formatted_leads

def _get_mocked_results(query, location):
    return [
        {
            "name": f"Mocked {query} 1",
            "category": query,
            "address": f"123 Street, {location}",
            "phone": "555-0101",
            "rating": 4.1,
            "reviews_count": 60,
            "website": "https://example.com"
        },
        {
            "name": f"Mocked {query} 2 (No Website)",
            "category": query,
            "address": f"456 Avenue, {location}",
            "phone": "555-0202",
            "rating": 3.2,
            "reviews_count": 12,
            "website": None
        },
        {
            "name": f"Mocked {query} 3",
            "category": query,
            "address": f"789 Road, {location}",
            "phone": None,
            "rating": 4.8,
            "reviews_count": 150,
            "website": None
        }
    ]
