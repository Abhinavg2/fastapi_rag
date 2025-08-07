import os
from PyPDF2 import PdfReader
from docx import Document

def read_docx(p): return "\n".join([p.text for p in Document(p).paragraphs])
def read_pdf(p): return "\n".join(page.extract_text() or "" for page in PdfReader(p).pages)

def chunk_text(text, max_words=500):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]

def chunk_documents(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    count = 0
    for fname in os.listdir(input_dir):
        path = os.path.join(input_dir, fname)
        text = read_docx(path) if fname.endswith(".docx") else read_pdf(path)
        for idx, chunk in enumerate(chunk_text(text)):
            out = os.path.join(output_dir, f"{fname}_{idx}.txt")
            with open(out, "w", encoding="utf-8") as f:
                f.write(chunk)
            count += 1
    return count
