from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama

from db_utils import add_documents_to_db, remove_index, remove_document, fetch_all
from files_utils import chunk_documents
from model_utils import rag_prompt

pdf_directory = "./data"

document_chunks = chunk_documents(pdf_directory=pdf_directory)

embedding = OllamaEmbeddings(model='mistral-7b-instruct-v0.1.Q5_K_M:latest')

db_kwargs = {
    "embedding": embedding,
    "es_url": "http://localhost:9200",
    "index_name": "rag",
    "distance_strategy": "COSINE"
}

remove_index(index_name=db_kwargs["index_name"], db_config={"hosts": db_kwargs["es_url"]})

db = add_documents_to_db(document_chunks=document_chunks,  db_kwargs=db_kwargs)


model = Ollama(model='mistral-7b-instruct-v0.1.Q5_K_M:latest')


response = rag_prompt(
    query = "",
    model=model,
    db=db,
)

# remove_document(
#     index_name=db_kwargs["index_name"],
#     source_file="",
#     db_config={"hosts": db_kwargs["es_url"]},
#     )

# fetch_all(
#     index_name=db_kwargs["index_name"],
#     db_config={"hosts": db_kwargs["es_url"]},
# )
