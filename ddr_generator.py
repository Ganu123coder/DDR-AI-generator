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
client = genai.Client(api_key=API_KEY)

# -------------------------------
# ✅ SAFE GENERATION FUNCTION
# -------------------------------
def safe_generate(prompt):
    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
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
            return "❌ API failed after retries"

        # safest response handling
        if hasattr(response, "text") and response.text:
            return response.text

        return "❌ Unexpected response format"

    except Exception as e:
        return f"❌ Error: {str(e)}"
