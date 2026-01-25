# prompt_rewriter.py
from google import genai
from google.genai import types
from config import GEMMA_API_KEY, LITE_MODEL

def rewrite_prompt(query):
    client = genai.Client(api_key=GEMMA_API_KEY)
    
   prompt = f"""
You are an expert intelligent query router for Class 9-10 NCTB textbooks.

First, decide:
- Does this question require searching specific lines from the textbook? (e.g., fact, author, plot detail, quote, definition, character action, specific event)
- Or is it general curiosity / explanation / opinion / overview / "tell me about" type?

Rules:
- If it needs textbook lines → Output 3–5 short, precise BANGLA search phrases (one per line)
- If it is general curiosity / overview → Output exactly: DIRECT_ANSWER_MODE
- Then, if DIRECT_ANSWER_MODE, rephrase the question naturally in Bangla for the main model.
- If search mode: use key nouns, writers, titles, characters, synonyms.
- Never invent facts.

Examples:
Original question: কপোতাক্ষ নদ কবিতার লেখক কে?
→ Search phrases (3–5 lines)

Original question: রবীন্দ্রনাথ ঠাকুর কে ছিলেন?
→ DIRECT_ANSWER_MODE
রবীন্দ্রনাথ ঠাকুর কে ছিলেন?

Original question: Photosynthesis কী?
→ DIRECT_ANSWER_MODE
Photosynthesis কী?

Original question: Who wrote Obhagir Shorgo?
→ Search phrases (3–5 lines)

Original question: ping
→ DIRECT_ANSWER_MODE
ping

Original question: {query}

Decision and Output:
"""
    
    response = client.models.generate_content(
        model=LITE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.05, max_output_tokens=100)
    )
    return response.text.strip()