from typing import List

from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def calculate_chunk_ids(chunks: List) -> List:

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks

def chunk_documents(pdf_directory: str) -> List: 
    document_loader = PyPDFDirectoryLoader(pdf_directory)
    document_chunks = document_loader.load_and_split(
        text_splitter=RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n"], chunk_size=1024, chunk_overlap=256
            # # Set chunk size and overlap as needed for your use case.
            # chunk_size=100,
            # chunk_overlap=20,
            # length_function=len,
            # separators=["."],  # Splitting primarily by dot, then by space and newline.
            # keep_separator=True,
            # is_separator_regex=False
        )
    )
    
    document_chunks = calculate_chunk_ids(document_chunks)
    
    return document_chunks


