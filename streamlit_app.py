import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from model_utils import rag_prompt
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms.ollama import Ollama

MODEL_NAME = "mistral-7b-instruct-v0.3.Q8_0:latest"

st.set_page_config(page_title="LLM with RAG system")
st.title("LLM with RAG system")

with st.chat_message("assistant"):
    st.write("Hello :)")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

model = Ollama(model=MODEL_NAME)
    
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
                    model=model,
                    db=db)
        st.markdown(ai_response)
        # uncomment after fixing get_response() and delete what is above
        #ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))
        
    st.session_state.chat_history.append(AIMessage(ai_response))