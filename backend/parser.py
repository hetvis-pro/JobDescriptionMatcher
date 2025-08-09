import PyPDF2
from docx import Document

def parse_docx(file_obj):
    doc = Document(file_obj)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


def parse_pdf(file_obj):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file_obj)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def parse_resume(file_obj):
    filename = file_obj.name.lower()

    if filename.endswith(".pdf"):
        return parse_pdf(file_obj)

    elif filename.endswith(".txt"):
        text = file_obj.read().decode("utf-8")
        return text.strip()

    elif filename.endswith(".docx"):
        return parse_docx(file_obj)

    else:
        raise ValueError("Unsupported resume file format.")

def parse_jd(file_obj):
    filename = file_obj.name.lower()

    if filename.endswith(".pdf"):
        return parse_pdf(file_obj)

    elif filename.endswith(".txt"):
        text = file_obj.read().decode("utf-8")
        return text.strip()

    elif filename.endswith(".docx"):
        return parse_docx(file_obj)

    else:
        raise ValueError("Unsupported JD file format.")
