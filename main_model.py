# main_model.py
from google import genai
from google.genai import types
import os
from config import MAIN_MODEL

def analyze_and_answer(original_query, context):
    api_key = os.getenv("GEMMA_API_KEY")
    if not api_key:
        raise ValueError("GEMMA_API_KEY not set in environment")
    
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
You are a Class 9-10 NCTB textbook teacher.
Answer based only on the provided context lines.
Use natural Bangla.
Cite sources naturally (e.g., পৃষ্ঠা ১৬৫ অনুযায়ী).
If direct answer: answer confidently.
If indirect but inferable: answer + one short disclaimer.
If not present: 'উত্তর তথ্যসূত্রে নেই।'

Context:
{context}

Question: {original_query}
Answer:
"""
    
    response = client.models.generate_content(
        model=MAIN_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=600)
    )
    return response.text.strip()
