import google.generativeai as genai
import os

key = os.environ.get('GEMINI_API_KEY')
print('API key present:', bool(key))

if not key:
    print('No key in env, trying .streamlit/secrets.toml...')
    try:
        import toml
        data = toml.load(os.path.join('.streamlit', 'secrets.toml'))
        key = data.get('GEMINI_API_KEY')
    except Exception as e:
        print('Could not load secrets.toml:', e)

try:
    genai.configure(api_key=key or "")
    models = list(genai.list_models())
    print("Retrieved models:")
    for m in models:
        print(m.name, getattr(m, 'supported_generation_methods', None))
except Exception as e:
    print('Error listing models:', e)
