from langchain_community.llms.ollama import Ollama
from langchain_elasticsearch import ElasticsearchStore

def rag_prompt(query: str, model: Ollama, db: ElasticsearchStore) -> str:
    results = db.similarity_search(query, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])

    # Format the prompt manually according to the template
    prompt = f"Kontekst: {context_text}\n\nPytanie: {query}"

    # Print the final prompt for debugging purposes
    print(prompt)

    # Directly invoke the model with the formatted prompt
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc in results]
    formatted_response = f"Odpowiedź: {response_text}\nŹródła: {sources}"

    print(formatted_response)

    return formatted_response