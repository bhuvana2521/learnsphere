import google.generativeai as genai
import os
import toml

def load_api_key():
    # Try env first
    key = os.environ.get('GEMINI_API_KEY')
    if key:
        return key
    # Fallback to streamlit secrets
    secrets_path = os.path.join('.streamlit', 'secrets.toml')
    if os.path.exists(secrets_path):
        data = toml.load(secrets_path)
        return data.get('GEMINI_API_KEY')
    return None

def main():
    api_key = load_api_key()
    if not api_key:
        print("No API key found. Set GEMINI_API_KEY in environment or .streamlit/secrets.toml")
        return

    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Configuration failed: {e}")
        return

    try:
        print("Listing available models:")
        models = list(genai.list_models())
        for m in models:
            print(" -", m.name)
    except Exception as e:
        print("Failed to list models:", e)
        models = []

    model_name = None
    for m in models:
        if "generateContent" in getattr(m, 'supported_generation_methods', []):
            model_name = m.name
            break

    if not model_name:
        print("No suitable model found.")
        return

    print(f"Using model: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print("Success! Response:")
        print(response.text)
    except Exception as e:
        print("Model invocation failed:", e)

if __name__ == "__main__":
    main()
