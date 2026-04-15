import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path
from prompt_template import get_prompt
import time

# -------------------------------
# ✅ FORCE CORRECT .env LOADING
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

# -------------------------------
# ❌ REMOVE CONFLICTING KEYS
# -------------------------------
os.environ.pop("GOOGLE_API_KEY", None)
os.environ.pop("API_KEY", None)

# -------------------------------
# ✅ GET CLEAN API KEY
# -------------------------------
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

print("DEBUG KEY:", repr(API_KEY))

# -------------------------------
# ❌ VALIDATION
# -------------------------------
if not API_KEY or "your_" in API_KEY:
    raise ValueError("❌ Invalid GEMINI_API_KEY. Fix your .env file")

print("✅ Using GEMINI API KEY:", API_KEY[:10], "...")

# -------------------------------
# ✅ INIT GEMINI CLIENT
# -------------------------------
genai.configure(api_key=API_KEY)

# -------------------------------
# ✅ SAFE GENERATION FUNCTION
# -------------------------------
def safe_generate(prompt):
    print("🔥 PROMPT SIZE:", len(prompt))

    try:
        print("🔥 Calling Gemini API...")

        response = model.generate_content(prompt)

        print("🔥 RESPONSE SUCCESS")
        print(response)

        return response

    except Exception as e:
        print("❌ GEMINI ERROR:", str(e))
        return None


# -------------------------------
# ✅ MAIN FUNCTION
# -------------------------------
def generate_ddr(inspection_text, thermal_text):
    try:
        prompt = get_prompt(inspection_text, thermal_text)

        response = safe_generate(prompt)

        if not response:
            return "❌ API failed after retries"

        # safest response handling
        if hasattr(response, "text") and response.text:
            return response.text

        return "❌ Unexpected response format"

    except Exception as e:
        return f"❌ Error: {str(e)}"
