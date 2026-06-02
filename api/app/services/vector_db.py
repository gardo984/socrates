import chromadb
import os
from sqlalchemy.orm import Session
from app.db.models import Document, DocumentChunk
from app.db.database import SessionLocal

# Langchain imports
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document as LangchainDocument

# Langchain Document Loaders
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader # Requires `unstructured` and its dependencies

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = os.getenv("CHROMA_PORT", "9000")
CHROMA_API_PORT = os.getenv("CHROMA_API_PORT", "8000") # Internal port for Chroma container

def get_chroma_client():
    # Use CHROMA_API_PORT for internal container communication
    return chromadb.HttpClient(host=CHROMA_HOST, port=int(CHROMA_API_PORT))

def load_and_extract_text(file_path: str, file_type: str) -> str:
    """
    Loads a document using the appropriate Langchain loader and extracts its full text.
    """
    documents = []
    try:
        if file_type == "txt":
            loader = TextLoader(file_path, encoding="utf-8")
        elif file_type == "pdf":
            loader = PyPDFLoader(file_path)
        elif file_type in ["doc", "docx"]: # UnstructuredWordDocumentLoader handles both
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            print(f"Unsupported file type for text extraction: {file_type}")
            return ""

        documents = loader.load()
        
        # Join the content of all pages/chunks loaded by Langchain loader
        full_text = " ".join([doc.page_content for doc in documents])
        return full_text

    except Exception as e:
        print(f"Error loading or extracting text from {file_path} ({file_type}): {e}")
        return ""

async def ingest_document_to_chroma(document_id: int, file_path: str):
    db: Session = SessionLocal()
    try:
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            print(f"Document {document_id} not found for ingestion.")
            return

        # Use the new loader function
        full_text = load_and_extract_text(file_path, document.file_type)
        if not full_text:
            print(f"No text extracted from {file_path}. Skipping ChromaDB ingestion.")
            return

        # Initialize Langchain text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        # Create Langchain Document objects from the text
        # You might already have a list of Langchain Documents if using `loader.load_and_split()`
        # For consistency with the `full_text` approach, we split the combined text.
        langchain_documents = text_splitter.create_documents([full_text], 
                                                             metadatas=[{"document_id": document_id, "filename": document.filename}])

        if not langchain_documents:
            print(f"No chunks generated from {file_text_path}. Skipping ChromaDB ingestion.")
            return

        # Initialize Langchain embedding model
        embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

        # Generate embeddings for each chunk
        texts = [doc.page_content for doc in langchain_documents]
        embeddings = embedding_model.embed_documents(texts)

        chroma_client = get_chroma_client()
        collection_name = f"document_{document_id}_chunks"
        collection = chroma_client.get_or_create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})

        ids = [f"chunk_{document_id}_{i}" for i in range(len(langchain_documents))]
        
        metadatas = []
        for i, doc in enumerate(langchain_documents):
            chunk_metadata = doc.metadata.copy()
            chunk_metadata["chunk_index"] = i
            metadatas.append(chunk_metadata)

        collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(texts)} chunks with embeddings to ChromaDB collection '{collection_name}' for doc {document_id}.")

        # Update the Document record with the ChromaDB collection ID
        document.chroma_collection_id = collection_name
        db.add(document)
        db.commit()
        db.refresh(document)
        print(f"Document {document_id} updated with chroma_collection_id: {collection_name}")

        # Store DocumentChunk entries in your relational DB
        for i, (chunk_text, vector_id) in enumerate(zip(texts, ids)):
            chunk_db_entry = DocumentChunk(
                document_id=document_id,
                chunk_index=i,
                content=chunk_text,
                chunk_size=len(chunk_text),
                vector_id=vector_id
            )
            db.add(chunk_db_entry)
        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error during ChromaDB ingestion for doc {document_id}: {e}")
    finally:
        db.close()