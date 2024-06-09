from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_elasticsearch import ElasticsearchStore


def rag_prompt(
    query: str,
    model: Ollama,
    db: ElasticsearchStore,
    ) -> str:
    PROMPT_TEMPLATE = """
    Odpowiedz na pytanie bazując tylko na poniższym kontekście:

    {context}

    ---

    Odpowiedz na to pytanie bazując na powyższym kontekście: {question}
    Odpowiedz w języku polskim
    """

    results = db.similarity_search(
        query, 
        k=5,
        )

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    
    prompt = prompt_template.format(context=context_text, question=query)
    
    print(prompt)

    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc in results]
    formatted_response = f"Odpowiedź: {response_text}\Źródła: {sources}"
    
    print(formatted_response)
    
    return formatted_response