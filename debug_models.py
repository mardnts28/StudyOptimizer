import os
from google import genai
from decouple import config

def list_models():
    api_key = config('GOOGLE_API_KEY')
    client = genai.Client(api_key=api_key)
    try:
        models = client.models.list()
        for m in models:
            print(m.name)
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
