import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path
from prompt_template import get_prompt
import time

# -------------------------------
# ✅ LOAD .ENV SAFELY
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

# -------------------------------
# ✅ GET API KEY (Render + Local safe)
# -------------------------------
API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

print("DEBUG KEY:", repr(API_KEY))

if not API_KEY or "your_" in API_KEY:
    raise ValueError("❌ Invalid GEMINI_API_KEY. Set it in Render or .env")

print("✅ Using GEMINI API KEY:", API_KEY[:10], "...")

# -------------------------------
# ✅ CONFIGURE GEMINI (OLD SDK STYLE)
# -------------------------------
genai.configure(api_key=API_KEY)

# -------------------------------
# ✅ MODEL
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
            return "❌ API failed after retries"

        if hasattr(response, "text") and response.text:
            return response.text

        return "❌ Unexpected response format"

    except Exception as e:
        return f"❌ Error: {str(e)}"