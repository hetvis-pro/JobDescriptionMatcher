import os
import requests
from backend.rag_engine import load_faiss_index
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TOGETHER_API_KEY")

def retrieve_relevant_chunks(user_query, top_k=4):
    resume_index = load_faiss_index("resume")
    jd_index = load_faiss_index("jd")

    resume_docs = resume_index.similarity_search(user_query, k=top_k)
    jd_docs = jd_index.similarity_search(user_query, k=top_k)

    all_docs = resume_docs + jd_docs
    context = "\n\n".join([doc.page_content for doc in all_docs])

    return context

def generate_llm_response(user_query, context, model="mistralai/Mistral-7B-Instruct-v0.1"):
    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a helpful assistant that answers questions about a resume and job description.

Context:
{context}

Question:
{user_query}

Answer:"""

    data = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        output = response.json()["output"]
        if isinstance(output, dict):
            return output["choices"][0]["text"].strip()
        return output.strip()

    except Exception as e:
        return f"❌ API Error: {str(e)}"

def chat_with_resume_and_jd(user_question):
    context = retrieve_relevant_chunks(user_question)
    answer = generate_llm_response(user_question, context)
    return answer
