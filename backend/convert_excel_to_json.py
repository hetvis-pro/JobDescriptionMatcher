import pandas as pd
import json

df = pd.read_excel("/data/Skills.xlsx")
skills = df["Element Name"].dropna().str.strip().str.lower().unique()
skills_list = sorted(skills)

with open("/data/skills_list.json", "w", encoding="utf-8") as f:
    json.dump(skills_list, f, indent=2)

print(f"✅ Saved {len(skills_list)} skills to data/skills_list.json")
