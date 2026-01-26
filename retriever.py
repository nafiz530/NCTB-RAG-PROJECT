# retriever.py
from index_store import LexicalIndex
from config import TOP_K

class CI:
    def __init__(self, lines):
        self.lines = lines
        self.top_k = TOP_K
        self.index = LexicalIndex(lines)   # ← This was missing

    def get_context(self, rewritten_queries_str, original_query="", detected_subject=None):
        queries = [q.strip() for q in rewritten_queries_str.split('\n') if q.strip()]
        if not queries:
            queries = [original_query]

        # Filter lines by subject if specified
        search_lines = self.lines
        if detected_subject and detected_subject != "সাধারণ/অজানা":
            search_lines = [l for l in self.lines if l.get("subject") == detected_subject]
            if not search_lines:
                search_lines = self.lines

        # Create temporary index for filtered lines (fast)
        temp_index = LexicalIndex(search_lines)

        collected = []
        seen = set()
        max_score = 0.0

        for q in queries:
            use_exact = '"' in q or len(q.split()) <= 5
            top_k_this = self.top_k if use_exact else self.top_k // 2 + 3

            lines_batch, scores = temp_index.retrieve(q, top_k=top_k_this, use_exact=use_exact)

            for line, score in zip(lines_batch, scores):
                text = line.get("text", "").strip()
                if text and text not in seen:
                    seen.add(text)
                    collected.append((line, score))
                    max_score = max(max_score, score)
                    if len(collected) >= self.top_k * 1.5:
                        break
            if max_score > 0.75 and len(collected) >= 3:
                break

        # Sort by score and select best
        collected.sort(key=lambda x: x[1], reverse=True)
        selected = [pair[0] for pair in collected[:self.top_k + 3]]

        # Format context
        context_parts = []
        for line in selected:
            title = line.get("title", "N/A")
            writer = line.get("writer", "N/A")
            page = line.get("book_page", "N/A")
            ref = f"(পাঠ্যবই: {title}, লেখক: {writer}, পৃষ্ঠা {page})"
            context_parts.append(f"- {line['text']}  {ref}")

        return "\n".join(context_parts) if context_parts else "কোনো প্রাসঙ্গিক লাইন পাওয়া যায়নি।"
