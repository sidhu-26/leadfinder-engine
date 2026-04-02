def calculate_lead_score(lead_data: dict) -> int:
    score = 0
    
    # No website → +50
    if not lead_data.get('has_website'):
        score += 50
        
    # Has phone → +20
    if lead_data.get('phone'):
        score += 20
        
    # Rating > 3.5 → +15
    rating = lead_data.get('rating')
    if rating and rating > 3.5:
        score += 15
        
    # Reviews > 50 → +15
    reviews_count = lead_data.get('reviews_count')
    if reviews_count and reviews_count > 50:
        score += 15
        
    return score
