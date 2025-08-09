from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return model.encode(text, convert_to_tensor=False)

def get_cosine_similarity(resume_text, jd_text):
    resume_vec = get_embedding(resume_text)
    jd_vec = get_embedding(jd_text)
    similarity = cosine_similarity([resume_vec], [jd_vec])
    return round(float(similarity[0][0]), 4)
