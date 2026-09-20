import google.generativeai as genai
import os
import toml

secrets_path = os.path.join('.streamlit','secrets.toml')
key=None
if os.path.exists(secrets_path):
    data = toml.load(secrets_path)
    key = data.get('GEMINI_API_KEY')
else:
    key = os.environ.get('GEMINI_API_KEY')
print('key loaded', bool(key))
if key:
    genai.configure(api_key=key)
try:
    models = list(genai.list_models())
    for m in models:
        print(m.name, getattr(m,'supported_generation_methods',None))
except Exception as e:
    print('error', e)
