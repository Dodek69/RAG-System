from typing import Dict, List

from langchain_elasticsearch import ElasticsearchStore
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from tqdm import tqdm



def add_documents_to_db(db: ElasticsearchStore, document_chunks: List,  db_kwargs: Dict) -> ElasticsearchStore:
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
