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
def generate_ddr(inspection_text, thermal_text, images):
    prompt = get_prompt(inspection_text, thermal_text)

    response = safe_generate(prompt)

    if not response:
        return "❌ Failed"

    report_text = response

    # 🔥 INSERT IMAGES INTO REPORT
    html_report = f"<h2>DDR Report</h2><p>{report_text}</p>"

    for img in images:
        img_base64 = image_to_base64(img)
        html_report += f"""
        <br>
        <img src="data:image/png;base64,{img_base64}" width="400"/>
        <br>
        """

    return html_report
