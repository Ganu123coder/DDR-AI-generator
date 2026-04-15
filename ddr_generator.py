import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from pathlib import Path
from prompt_template import get_prompt

# -------------------------------
# ✅ LOAD .ENV PROPERLY
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

# -------------------------------
# ✅ GET API KEY (LOCAL + RENDER SAFE)
# -------------------------------
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

print("🔍 DEBUG KEY:", repr(API_KEY))

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found. Set it in .env or Render environment variables")

print("✅ GEMINI API KEY LOADED:", API_KEY[:10], "...")

# -------------------------------
# ✅ CONFIGURE GEMINI (OLD SDK - STABLE)
# -------------------------------
genai.configure(api_key=API_KEY)

# -------------------------------
# ✅ MODEL INIT
# -------------------------------
model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------
# ✅ SAFE GENERATION FUNCTION
# -------------------------------
def safe_generate(prompt):
    for i in range(3):
        try:
            response = model.generate_content(prompt)
            return response
        except Exception as e:
            print(f"⚠️ Retry {i+1}/3 failed:", str(e))
            time.sleep(2)

    return None

# -------------------------------
# ✅ MAIN FUNCTION
# -------------------------------
def generate_ddr(inspection_text, thermal_text):
    try:
        prompt = get_prompt(inspection_text, thermal_text)

        response = safe_generate(prompt)

        if not response:
            return "❌ API failed after 3 retries"

        # safe output handling
        if hasattr(response, "text") and response.text:
            return response.text

        return "❌ Unexpected response format from Gemini API"

    except Exception as e:
        return f"❌ Error occurred: {str(e)}"