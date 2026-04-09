import requests
from requests.auth import HTTPBasicAuth
from decouple import config

def test_cloudinary_credentials():
    cloud_name = config('CLOUDINARY_CLOUD_NAME')
    api_key    = config('CLOUDINARY_API_KEY')
    api_secret = config('CLOUDINARY_API_SECRET')
    
    # We use the Admin API to list resources which requires Basic Auth (API_KEY:API_SECRET)
    # This is the standard way to test if credentials are valid.
    url = f"https://api.cloudinary.com/v1_1/{cloud_name}/resources/image"
    
    print(f"DEBUG: Testing Cloudinary credentials for cloud: {cloud_name}")
    print(f"DEBUG: Using API Key: {api_key}")
    
    try:
        response = requests.get(url, auth=HTTPBasicAuth(api_key, api_secret))
        
        if response.status_code == 200:
            print("SUCCESS: Cloudinary credentials are 100% CORRECT!")
            print(f"Account returned {len(response.json().get('resources', []))} images.")
        else:
            print(f"FAILURE: Cloudinary returned {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: Connection failed: {e}")

if __name__ == "__main__":
    test_cloudinary_credentials()
