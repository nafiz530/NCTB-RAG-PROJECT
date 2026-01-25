# config.py
import os

GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")  # Set this in Colab secrets

SUBJECT_MAP = {
    "bangla_9-10_bangla_1st_sentence.jsonl": "বাংলা ১ম পত্র",
    "bangla_9-10_bangla_2nd_sentence.jsonl": "বাংলা ২য় পত্র",
    "bangla_9-10_bangla_sohopath_sentence.jsonl": "বাংলা সহপাঠ",
    "bangla_9-10_english_1st_sentence.jsonl": "ইংরেজি ১ম পত্র",
    "bangla_9-10_english_2nd_sentence.jsonl": "ইংরেজি ২য় পত্র",
    "bangla_9-10_mathematics_sentence.jsonl": "গণিত",
    "bangla_9-10_higher_math_sentence.jsonl": "উচ্চতর গণিত",
    "bangla_9-10_ict_sentence.jsonl": "তথ্য ও যোগাযোগ প্রযুক্তি",
    "bangla_9-10_physics_sentence.jsonl": "পদার্থবিজ্ঞান",
    "bangla_9-10_chemistry_sentence.jsonl": "রসায়ন",
    "bangla_9-10_biology_sentence.jsonl": "জীববিজ্ঞান",
    "bangla_9-10_bgs_sentence.jsonl": "বাংলাদেশ ও বিশ্বপরিচয়",
    "bangla_9-10_islam_sentence.jsonl": "ইসলাম শিক্ষা",
    "bangla_9-10_hindu_sentence.jsonl": "হিন্দু ধর্ম শিক্ষা",
    "bangla_9-10_physical_education_sentence.jsonl": "শারীরিক শিক্ষা",
    "bangla_9-10_career_education_sentence.jsonl": "ক্যারিয়ার শিক্ষা",
}

DATA_PATHS = [f"data/{f}" for f in SUBJECT_MAP.keys()]

TOP_K = 10
LITE_MODEL = "gemma-3-12b-it"
MAIN_MODEL = "gemma-3-27b-it"