import re

def highlight_text(text, keywords, color):
    for kw in sorted(keywords, key=lambda x: -len(x)):  # Match longest terms first
        pattern = re.compile(rf"(?i)\b({re.escape(kw)})\b")
        text = pattern.sub(rf'<span style="background-color:{color}; font-weight:bold">\1</span>', text)
    return text

def generate_highlighted_text(resume_text, jd_text, match_data):
    matched = match_data["matched"]
    missing = match_data["missing"]

    resume_highlighted = highlight_text(resume_text, matched, "#d4edda")   # green
    jd_highlighted     = highlight_text(jd_text, matched, "#d4edda")       # green
    jd_highlighted     = highlight_text(jd_highlighted, missing, "#f8d7da")  # red

    return resume_highlighted, jd_highlighted
