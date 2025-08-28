import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.parser import parse_resume, parse_jd
from backend.embeddings import get_cosine_similarity

resume_text = parse_resume("/data/attorney-resume-example.pdf")
jd_text = parse_jd("/data/JD3.txt")

similarity = get_cosine_similarity(resume_text, jd_text)
print(f"Cosine Similarity Score: {similarity * 100:.2f}%")
