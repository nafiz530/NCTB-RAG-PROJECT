# main_model.py
from google import genai
from google.genai import types
from config import GEMMA_API_KEY, MAIN_MODEL

def analyze_and_answer(original_query, context):
    client = genai.Client(api_key=GEMMA_API_KEY)
    
    prompt = f"""
You are a Class 9-10 NCTB textbook teacher.

Context provided:
{context}

Special mode detection:
- If the context is empty, very short, or contains "DIRECT_ANSWER_MODE" → This is a general curiosity question.
  → Answer using your knowledge + textbook understanding.
  → Use book references where possible (e.g., "পাঠ্যবইয়ে ... অংশে বলা হয়েছে").
  → Do not say "উত্তর তথ্যসূত্রে নেই।" for curiosity questions.
  → Be educational, helpful, and accurate.
  → Enhance the answer naturally without changing core facts.

- If context contains real book lines → Answer strictly based on those lines.
  → Cite sources naturally (e.g., পৃষ্ঠা ১৬৫ অনুযায়ী).
  → If direct match → answer confidently.
  → If indirect but inferable → answer + one soft disclaimer.
  → If truly not present → 'উত্তর তথ্যসূত্রে নেই।'

Question: {original_query}
Answer in natural, student-friendly Bangla:
"""
    
    response = client.models.generate_content(
        model=MAIN_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=600)
    )
    return response.text.strip()