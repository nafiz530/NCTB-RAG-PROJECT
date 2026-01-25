# question.py
from data_loader import load_lines
from retriever import CI
from prompt_rewriter import rewrite_prompt
from main_model import analyze_and_answer
from subject_detector import detect_subject

def run_questions(questions):
    lines = load_lines()
    ci = CI(lines)
    
    for i, q in enumerate(questions, 1):
        print(f"\n🔹 Question {i}: {q}")
        subject = detect_subject(q)
        print(f"   Subject: {subject}")
        
        rewritten = rewrite_prompt(q)
        print(f"   Rewritten: {rewritten}")
        
        if "Invalid query" in rewritten:
            print("   Answer: দয়া করে বৈধ প্রশ্ন দিন।")
            continue
        
        context = ci.get_context(rewritten, q, subject)
        answer = analyze_and_answer(q, context)
        print(f"   Answer: {answer[:500]}{'...' if len(answer) > 500 else ''}")

if __name__ == "__main__":
    questions = [
        "কপোতাক্ষ নদ কবিতার লেখক কে?",
        "Photosynthesis কী?",
        "Who wrote Obhagir Shorgo story?",
        "অভাগীর স্বর্গ গল্পে কাঙালীর মায়ের শেষ ইচ্ছা কী?",
        "What is the last wish of Kangali's mother in Obhagir Swargo?"
    ]
    run_questions(questions)