from langchain_community.llms.ollama import Ollama
from langchain_elasticsearch import ElasticsearchStore

def rag_prompt(query: str, model: Ollama, db: ElasticsearchStore, context_char_threshold: int, chunker_type: str) -> str:
    results = db.similarity_search(query, k=5, fetch_k=100)
    context_texts = []
    current_length = 0
    
    for doc in results:
        doc_length = len(doc.page_content)
        if current_length + doc_length > context_char_threshold and chunker_type=="semantic":
            break
        context_texts.append(doc.page_content)
        current_length += doc_length
        
    print(f"Selected {len(context_texts)} documents with a total length of {current_length} characters.")

    context_text = "\n\n---\n\n".join(context_texts)

    # Format the prompt manually according to the template
    prompt = f"Kontekst: {context_text}\n\nPytanie: {query}"
    
    # Print the final prompt for debugging purposes
    print(prompt)

    # Directly invoke the model with the formatted prompt
    response_text = model.invoke(prompt)

    sources = [str(doc.metadata.get("page", None)) for doc in results[:len(context_texts)]]
    # sources = [doc.metadata.get("id", None) for doc in results[:len(context_texts)]]
    sources_str = '\n'.join(sources)
    formatted_response = f"{response_text}\n\nŹródła:\n\n{sources_str}"
    return formatted_response