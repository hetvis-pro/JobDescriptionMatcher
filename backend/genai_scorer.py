import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")
# def get_genai_match_score(resume_text, jd_text):
#     prompt = f"""
# You are a helpful resume screening assistant.

# Given the following resume and job description, assess how well the resume matches the job. Provide a match score out of 100 and a detailed explanation.

# Resume:
# {resume_text}

# Job Description:
# {jd_text}

# Respond in the format:
# Match Score: <score>/100
# Reason: <your reasoning>
# """

#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={"model": "gemma:2b", "prompt": prompt, "stream": False}
#         )

#         response.raise_for_status()  # Raise error for HTTP issues

#         data = response.json()
#         return data.get("response", "Error: No response content.")

#     except requests.exceptions.RequestException as e:
#         return f"❌ Error: {e}"



def get_genai_match_score(resume_text, jd_text):
    prompt = f"""
You are a helpful resume screener for recruiters.

Given the following RESUME and JOB DESCRIPTION, analyze how well the resume matches the role.

Give a score out of 100, and explain what skills match and what is missing.

Resume:
{resume_text}

Job Description:
{jd_text}

Respond in the following format:
Match Score: <score>/100
Reason: <your reasoning here>
"""

    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "temperature": 0.3,
        "max_tokens": 512
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()["output"]
        if isinstance(output, dict):
            return output["choices"][0]["text"].strip()
        return output.strip()
    except Exception as e:
        return f"❌ API Error: {str(e)}"