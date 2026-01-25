# data_loader.py
import json
import os
from config import DATA_PATHS, SUBJECT_MAP

def load_lines():
    lines = []
    for path in DATA_PATHS:
        filename = os.path.basename(path)
        subject = SUBJECT_MAP.get(filename, "অজানা বিষয়")
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line.strip())
                        data["subject"] = subject
                        data["source_file"] = filename
                        lines.append(data)
        except Exception as e:
            print(f"⚠️ Error loading {filename}: {e}")
    print(f"✅ Loaded {len(lines)} lines from {len(DATA_PATHS)} subjects")
    return lines