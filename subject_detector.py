# subject_detector.py
from google import genai
from google.genai import types
import os
from config import LITE_MODEL, SUBJECT_MAP

def detect_subject(query):
    if not query or len(query) < 3:
        return "সাধারণ/অজানা"
    
    api_key = os.getenv("GEMMA_API_KEY")
    if not api_key:
        raise ValueError("GEMMA_API_KEY not set in environment")
    
    client = genai.Client(api_key=api_key)
    subjects_list = "\n".join([f"- {s}" for s in SUBJECT_MAP.values()])
    
    prompt = f"""
Classify the subject of this student question into one from the list below.
Output ONLY the exact subject name.

List:
{subjects_list}

Question: {query}

Subject:
"""
    
    try:
        response = client.models.generate_content(
            model=LITE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=15)
        )
        detected = response.text.strip()
        if detected in SUBJECT_MAP.values():
            return detected
    except:
        pass
    return "সাধারণ/অজানা"
