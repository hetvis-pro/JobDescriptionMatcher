import os
import tempfile
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Hugging Face Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Split long text into chunks
def split_into_chunks(text, source_name):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    docs = splitter.create_documents([text])
    for doc in docs:
        doc.metadata["source"] = source_name
    return docs

# Create FAISS index from text chunks
def create_faiss_index_from_text(text, source_name):
    documents = split_into_chunks(text, source_name)
    faiss_index = FAISS.from_documents(documents, embedding_model)
    return faiss_index

# Save FAISS index to disk temporarily
def save_faiss_index(faiss_index, name_prefix):
    temp_dir = tempfile.gettempdir()
    index_path = os.path.join(temp_dir, f"{name_prefix}_faiss_index")
    faiss_index.save_local(index_path)
    return index_path

# Load FAISS index from disk
def load_faiss_index(name_prefix):
    temp_dir = tempfile.gettempdir()
    index_path = os.path.join(temp_dir, f"{name_prefix}_faiss_index")
    return FAISS.load_local(index_path, embedding_model, allow_dangerous_deserialization=True)
