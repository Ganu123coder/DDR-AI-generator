import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
from pathlib import Path
from prompt_template import get_prompt

# -------------------------------
# ✅ LOAD ENV
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not set")

print("✅ API KEY LOADED")

# -------------------------------
# ✅ CONFIGURE GEMINI
# -------------------------------
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------
# ✅ SAFE GENERATE (ROBUST VERSION)
# -------------------------------
def safe_generate(prompt):
    try:
        # 🔥 LIMIT PROMPT SIZE (VERY IMPORTANT)
        prompt = prompt[:8000]

        print("📏 Prompt Length:", len(prompt))

        response = model.generate_content(prompt)

        # 🔥 SAFE RESPONSE PARSING
        if hasattr(response, "text") and response.text:
            return response.text

        # fallback (sometimes needed)
        if response.candidates:
            return response.candidates[0].content.parts[0].text

        return "❌ Empty response from Gemini"

    except Exception as e:
        print("❌ GEMINI ERROR:", str(e))
        return f"❌ Gemini API Error: {str(e)}"


# -------------------------------
# ✅ MAIN FUNCTION
# -------------------------------
def generate_ddr(inspection_text, thermal_text):
    try:
        prompt = get_prompt(inspection_text, thermal_text)

        result = safe_generate(prompt)

        return result

    except Exception as e:
        return f"❌ Error occurred: {str(e)}"
