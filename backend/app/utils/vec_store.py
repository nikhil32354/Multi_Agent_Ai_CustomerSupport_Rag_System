"""Vector store ingestion utilities (placeholder)
Use LangChain + pgvector for real ingestion.
"""
import os
from pathlib import Path
from ..core.config import settings

try:
    from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
    from langchain_community.vectorstores.pgvector import PGVector
    from langchain_openai import OpenAIEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except Exception:
    TextLoader = PyPDFLoader = Docx2txtLoader = None
    PGVector = None
    OpenAIEmbeddings = None
    RecursiveCharacterTextSplitter = None
    LANGCHAIN_AVAILABLE = False


def ingest_document(file_path: str, collection_name: str = 'kb'):
    # support plain text, PDF, and DOCX files
    if not os.path.exists(file_path):
        return {'status': 'error', 'reason': 'file not found'}

    if not LANGCHAIN_AVAILABLE:
        return {'status': 'skipped', 'reason': 'langchain integrations are not installed'}

    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        loader = PyPDFLoader(file_path)
    elif ext in ('.docx', '.doc'):
        loader = Docx2txtLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding='utf-8')

    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    # create or connect to PGVector (table/collection name 'kb')
    PGVector.from_documents(chunks, embeddings, connection_string=settings.database_url, collection_name=collection_name)
    return {'status': 'ingested', 'count': len(chunks), 'collection': collection_name}
