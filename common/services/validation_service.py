import requests

def check_website_exists(url: str) -> bool:
    if not url:
        return False
        
    try:
        # Add a timeout and generic headers
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.head(url, timeout=5, headers=headers, allow_redirects=True)
        return response.status_code < 400
    except requests.RequestException:
        # Retry with GET if HEAD fails
        try:
            response = requests.get(url, timeout=5, headers=headers)
            return response.status_code < 400
        except requests.RequestException:
            return False
