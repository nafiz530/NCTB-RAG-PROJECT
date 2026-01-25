# test_batch.py
"""
Batch test script for NCTB-RAG-PROJECT
Runs a list of questions automatically and prints results.
Good for first validation after adding 16 subjects.
"""

from data_loader import load_lines
from subject_detector import detect_subject
from prompt_rewriter import rewrite_prompt
from retriever import CI
from main_model import analyze_and_answer
from config import TOP_K

def run_batch_test(questions=None):
    print("=== NCTB RAG Batch Test ===")
    print("Loading all subjects...\n")
    
    lines = load_lines()
    if not lines:
        print("ERROR: No lines loaded. Check data/ folder and paths.")
        return
    
    print(f"Total lines loaded: {len(lines):,}")
    print(f"Running {len(questions or [])} questions...\n")
    
    ci = CI(lines)
    
    questions = questions or [
        "কপোতাক্ষ নদ কবিতার লেখক কে?",
        "Photosynthesis কী?",
        "অভাগীর স্বর্গ গল্পে কাঙালীর মায়ের শেষ ইচ্ছা কী?",
        "Who is the author of Kopotakkho Nod poem?",
        "রবীন্দ্রনাথ ঠাকুর কে ছিলেন?",
        "What is the main theme of 'Manush' poem by Kazi Nazrul Islam?",
        "পদার্থবিজ্ঞানে গতি কী?",
        "ping",
    ]
    
    for i, q in enumerate(questions, 1):
        print(f"\n┌─ Question {i}/{len(questions)}")
        print(f"│  {q}")
        
        subject = detect_subject(q)
        print(f"│  Detected subject → {subject}")
        
        rewritten = rewrite_prompt(q)
        print(f"│  Rewritten queries:\n│  {rewritten.replace('\n', '\n│  ')}")
        
        if "Invalid query" in rewritten:
            print("└─ Answer: দয়া করে বৈধ প্রশ্ন দিন।")
            continue
        
        context = ci.get_context(rewritten, q, detected_subject=subject)
        line_count = len([l for l in context.split('\n') if l.strip().startswith('-')])
        print(f"│  Retrieved {line_count} relevant lines")
        
        answer = analyze_and_answer(q, context)
        print(f"│")
        print(f"└─ Answer:\n{answer}")
        print("─" * 70)

if __name__ == "__main__":
    run_batch_test()