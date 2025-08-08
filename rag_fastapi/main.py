from fastapi import FastAPI, UploadFile, File, HTTPException
from .utils.file_handler import save_uploaded_file
from .utils.chunker import chunk_documents
from .utils.embedder import embed_to_search
from .utils.responder import answer_query
from pydantic import BaseModel

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only .pdf and .docx allowed")
    path = await save_uploaded_file(file)
    return {"message": "Uploaded", "path": path}

@app.post("/process")
def process():
    count = chunk_documents("uploaded_files", "processed_chunks")
    return {"message": f"Created {count} chunks"}

@app.post("/embed")
def embed():
    count = embed_to_search("processed_chunks")
    return {"message": f"Indexed {count} documents"}

class Query(BaseModel):
    question: str

@app.post("/response")
def respond(query: Query):
    answer = answer_query(query.question)
    return {"answer": answer}

