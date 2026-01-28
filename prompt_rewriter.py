# prompt_rewriter.py
from google import genai
from google.genai import types
import os
from config import LITE_MODEL

def rewrite_prompt(query):
    api_key = os.getenv("GEMMA_API_KEY")
    if not api_key:
        raise ValueError("GEMMA_API_KEY not set in environment")
    
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
You are an expert search optimizer for Class 9-10 NCTB textbooks.
Convert the question (Bangla or English) into 3–5 short, precise BANGLA search phrases.

Rules:
- Translate English to natural Bangla if needed.
- Output ONLY 3–5 Bangla phrases, one per line.
- Include key nouns: subject, topic, writer, character, term.
- Keep phrases 4–12 words.
- If invalid/nonsense: output exactly "Invalid query"

Original question: {query}

Search phrases:
"""
    
    response = client.models.generate_content(
        model=LITE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.05, max_output_tokens=100)
    )
    return response.text.strip()
