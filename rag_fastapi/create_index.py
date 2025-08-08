from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType
)

import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

# Initialize Search Client
index_client = SearchIndexClient(endpoint=search_endpoint,
                                 credential=AzureKeyCredential(search_key))

# Define schema
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String),
    SimpleField(name="chunk_id", type=SearchFieldDataType.String, filterable=True),
    SimpleField(name="source", type=SearchFieldDataType.String, filterable=True)
]

index = SearchIndex(name=index_name, fields=fields)

# Delete the index if it exists
if index_name in [idx.name for idx in index_client.list_indexes()]:
    index_client.delete_index(index_name)
    print(f"🗑️ Deleted existing index '{index_name}'")

# Create new index
result = index_client.create_index(index)
print(f"✅ Created new index: {result.name}")
