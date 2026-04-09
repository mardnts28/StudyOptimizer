
import os
import django
from decouple import config
from google import genai

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyoptimizer.settings')
django.setup()

def test_ai():
    api_key = config('GOOGLE_API_KEY', default='').strip()
    if not api_key:
        print("MISSING API KEY")
        return
    
    print(f"Testing with API Key: {api_key[:10]}...")
    client = genai.Client(api_key=api_key)
    
    try:
        response = client.models.generate_content(
            model='models/gemini-2.0-flash',
            contents="Hello, say 'AI is working' if you can read this."
        )
        print("RESPONSE:", response.text)
    except Exception as e:
        print("ERROR:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai()
