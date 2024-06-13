from typing import Dict, List

from langchain_elasticsearch import ElasticsearchStore
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from tqdm import tqdm
import os
import atexit
import shutil
import glob
from files_utils import chunk_documents


def add_documents_to_db(db: ElasticsearchStore, document_chunks: List, db_kwargs: Dict, bulk_upload: bool = True) -> ElasticsearchStore:
    if bulk_upload:
        print("Bulk ingesting documents...")
        if db:
            db.add_documents(document_chunks)
        else:
            db = ElasticsearchStore.from_documents(document_chunks, **db_kwargs)
    else:
        with tqdm(total=len(document_chunks), desc="Ingesting documents") as pbar:
            for chunk in document_chunks:
                if db:
                    db.add_documents([chunk])
                else:
                    db = ElasticsearchStore.from_documents([chunk], **db_kwargs)
                pbar.update(1)
                
    return db
            
            
def remove_index(index_name: str, db_config: Dict) -> None:

    es = Elasticsearch(**db_config)

    try:
        response = es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted successfully.")
    except NotFoundError:
        print(f"Index '{index_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def remove_document(index_name: str, source_file: str, db_config: Dict) -> None:
    
    es = Elasticsearch(**db_config)

    query = {
        "query": {
            "term": {
                "metadata.source.keyword": source_file
            }
        }
    }

    try:
        response = es.delete_by_query(index=index_name, body=query)
        print(f"Documents with source '{source_file}' deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def fetch_all(index_name: str, db_config: Dict) -> None:
    es = Elasticsearch(**db_config)

    query = {
        "query": {
            "match_all": {}
        }
    }

    try:
        all_documents = []

        response = es.search(index=index_name, body=query, scroll='2m', size=1000)
        scroll_id = response['_scroll_id']
        all_documents.extend(response['hits']['hits'])

        while len(response['hits']['hits']) > 0:
            response = es.scroll(scroll_id=scroll_id, scroll='2m')
            scroll_id = response['_scroll_id']
            all_documents.extend(response['hits']['hits'])

        print(f"Retrieved {len(all_documents)} documents.")

        for doc in all_documents:
            del doc['_source']["vector"]
            print(doc['_source'])

    except Exception as e:
        print(f"An error occurred: {e}")
        

def clear_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if filename != ".placeholder":
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted {filename}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted directory {filename}")
    except Exception as e:
        print(f"Error clearing folder: {e}")

def search_pdf_in_subfolders(directory, pdf_filename):
    found = False
    search_pattern = os.path.join(directory, '**', pdf_filename)
    pdf_files = glob.glob(search_pattern, recursive=True)
    
    if pdf_files:
        found = True
        print(f"Found {pdf_filename} in:")
        for file_path in pdf_files:
            print(f"- {file_path}")
    
    return found

def upload_files(uploaded_files, db_kwargs, model_name):
    SAVE_DIR = os.path.join('data', 'uploaded')
    TEMP_DIR = os.path.join('data', 'temp')
    if uploaded_files:
        for file in uploaded_files:
            if not search_pdf_in_subfolders('data', file.name):
                file_path = os.path.join(TEMP_DIR, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

                file_path = os.path.join(SAVE_DIR, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

    pdf_directory = "./data/temp"
    document_chunks = chunk_documents(pdf_directory=pdf_directory, model_name=model_name)
    add_documents_to_db(db=None, document_chunks=document_chunks, db_kwargs=db_kwargs, bulk_upload=True)
    clear_folder(pdf_directory)