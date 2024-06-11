# RAG-System
This project showcases the implementation of a Retrieval-Augmented Generation (RAG) system, combining the power of a vector database and a language model to enhance information retrieval and generation capabilities.


## Model prep:

install ollama https://ollama.com/download 
`curl -fsSL https://ollama.com/install.sh | sh` (on linux)

Download:
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

model: `mistral-7b-instruct-v0.1.Q5_K_M.gguf`

```sh
cp mistral-7b-instruct-v0.1.Q5_K_M.gguf ./models 
cd models
ollama create mistral-7b-instruct-v0.1.Q5_K_M -f ./mistral-7b-instruct-v0.1.Q5_K_M
ollama run mistral-7b-instruct-v0.1.Q5_K_M
```

## ElasticSearch db prep:

```sh
docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.12.1
```

## Streamlit:

```sh
pip install streamlit

streamlit run streamlit_app.py --server.port 8502
```