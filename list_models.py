
import os
import django
from decouple import config
from google import genai

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studyoptimizer.settings')
django.setup()

def list_models():
    api_key = config('GOOGLE_API_KEY', default='').strip()
    client = genai.Client(api_key=api_key)
    
    try:
        print("Available models:")
        for m in client.models.list():
            print(f"- {m.name}")
    except Exception as e:
        print("ERROR listing models:", e)

if __name__ == "__main__":
    list_models()
