import spacy
import json

# Load skills list from saved JSON(generated from Excel)
with open("/data/skills_list.json", "r", encoding="utf-8") as f:
    SKILLS = set(json.load(f))

nlp = spacy.load("en_core_web_sm")

def extract_skills(text):
    doc = nlp(text.lower())
    extracted_skills = set()

    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.strip()
        if chunk_text in SKILLS:
            extracted_skills.add(chunk_text)

    for token in doc:
        if token.text in SKILLS:
            extracted_skills.add(token.text)

    return extracted_skills

def compare_skills(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills.difference(resume_skills)

    return {
        "matched": matched,
        "missing": missing,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills
    }
