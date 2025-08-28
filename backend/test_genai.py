import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.parser import parse_resume, parse_jd
from backend.genai_scorer import get_genai_match_score

resume_text = parse_resume("/data/attorney-resume-example.pdf")
jd_text = parse_jd("/data/JD1.txt")

result = get_genai_match_score(resume_text, jd_text)
print("\n Match Result:\n", result)
