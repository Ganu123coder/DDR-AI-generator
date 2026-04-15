def get_prompt(inspection_text, thermal_text):
    return f"""
You are an expert building inspection analyst.

Using the provided Inspection Report and Thermal Report,
generate a Detailed Diagnostic Report (DDR).

RULES:
- Do NOT invent facts
- If missing → write "Not Available"
- If conflict → mention conflict
- Avoid duplicates
- Use simple client-friendly language

STRUCTURE:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment (with reasoning)
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

Inspection Report:
{inspection_text}

Thermal Report:
{thermal_text}
"""