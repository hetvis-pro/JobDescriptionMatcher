import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.parser import parse_resume, parse_jd

resume_text = parse_resume("/data/attorney-resume-example.pdf")
jd_text = parse_jd("/data/JD3.txt")

print("=== RESUME TEXT ===")
print(resume_text[:1000]) 
print("\n=== JD TEXT ===")
print(jd_text[:1000])
