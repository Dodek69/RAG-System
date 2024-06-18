from typing import List
import logging
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents.base import Document

def process_document(document: Document, chunker) -> List[Document]:
    result = []
    
    # Extract text and metadata from the document object
    doc_text = document.page_content if hasattr(document, 'page_content') else str(document)
    source = document.metadata.get("source", "unknown_source")
    page = document.metadata.get("page", "unknown_page")
    
    # Split text into chunks
    chunks = chunker.split_text(doc_text)
    
    last_page_id = None
    current_chunk_index = 0
    
    for i, chunk_text in enumerate(chunks):
        current_page_id = f"{source}:{page}"
        
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
        
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        
        # Create a Document object for each chunk
        chunk = Document(
            page_content=chunk_text,
            metadata={
                "source": source,
                "page": page,
                "id": chunk_id
            }
        )
        result.append(chunk)
        
    return result
    
    
def chunk_documents(pdf_directory: str, chunker_type: str) -> List[Document]:
    """
    Loads and splits PDF documents into semantic chunks using local embeddings.

    Args:
        pdf_directory (str): Path to the directory containing PDF documents.
        chunker_type (str): The name of the chuning method.

    Returns:
        List[Document]: A list of document chunks with calculated IDs.
    """
    try:
        # Initialize the document loader
        document_loader = PyPDFDirectoryLoader(pdf_directory, recursive=True)
        
        
        # Load the documents
        documents = document_loader.load()
        
        print(f"Loaded {len(documents)} documents." if documents else "No documents found.")
        
        
        if chunker_type == "semantic":
            embedding = FastEmbedEmbeddings()
            chunker = SemanticChunker(embedding)
        else:
            chunker = RecursiveCharacterTextSplitter(
                chunk_size=400,
                chunk_overlap=200,
                length_function=len,
                is_separator_regex=False,
            )
        
        all_chunks = []
        for doc in documents:
            # Process each document
            chunks = process_document(document=doc, chunker=chunker)
            all_chunks.extend(chunks)

        return all_chunks
    
    except Exception as e:
        logging.error(f"An error occurred while chunking documents: {e}")
        return []