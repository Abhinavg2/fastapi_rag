import os
import re
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

# Azure Search client
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

def sanitize_id(filename):
    # Replace all non-allowed characters with underscore
    return re.sub(r'[^a-zA-Z0-9_\-=]', '_', filename)

def embed_to_search(chunk_folder):
    documents = []
    for fname in os.listdir(chunk_folder):
        with open(os.path.join(chunk_folder, fname), "r", encoding="utf-8") as f:
            text = f.read()
        safe_id = sanitize_id(fname)
        documents.append({
            "id": safe_id,
            "content": text,
            "chunk_id": fname.split("_")[0],
            "source": "uploaded"
        })
    result = search_client.upload_documents(documents)
    return len(result)
