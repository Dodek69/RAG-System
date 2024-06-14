import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from model_utils import rag_prompt
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from config import MODEL_NAME
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama
from db_utils import add_documents_to_db, remove_index, remove_document, fetch_all, upload_files, clear_folder
from files_utils import chunk_documents
from model_utils import rag_prompt
from langchain_elasticsearch import ElasticsearchStore
from langchain_community.embeddings import OllamaEmbeddings
from config import MODEL_NAME, ES_PORT, ES_INDEX_NAME, ES_DISTANCE_STRATEGY
import os
import atexit

st.set_page_config(page_title="LLM with RAG system")
st.title("LLM with RAG system")

# Uplaod files
uploaded_files = st.file_uploader(label = 'Upload your pdf files', accept_multiple_files=True, type='pdf')


EMBEDDING = OllamaEmbeddings(model=MODEL_NAME)
DB_KWARGS = {
    "embedding": EMBEDDING,
    "es_url": f"http://localhost:{ES_PORT}",
    "index_name": ES_INDEX_NAME,
    "distance_strategy": ES_DISTANCE_STRATEGY,
}
DB = ElasticsearchStore(**DB_KWARGS)
MODEL = Ollama(model=MODEL_NAME)

upload_files(uploaded_files, DB_KWARGS, MODEL_NAME)


# chat with LLM
with st.chat_message("assistant"):
    st.write("Hello :)")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# conversation
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

# user input
user_query = st.chat_input("Your message")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        #ai_response = "0111 0110 1110 111 000 [...] - translating to human language -> Napraw mnie....."
        ai_response = rag_prompt(
                    query = user_query,
                    model=MODEL,
                    db=DB)
        st.markdown(ai_response)
        # uncomment after fixing get_response() and delete what is above
        #ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))
        
    st.session_state.chat_history.append(AIMessage(ai_response))
    
# flush temp folder
atexit.register(clear_folder, './data/temp')