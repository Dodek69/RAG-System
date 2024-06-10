# RAG-System
This project showcases the implementation of a Retrieval-Augmented Generation (RAG) system, combining the power of a vector database and a language model to enhance information retrieval and generation capabilities.


## Model prep:

Download:
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

model: `mistral-7b-instruct-v0.1.Q5_K_M.gguf`

```sh
cp mistral-7b-instruct-v0.1.Q5_K_M.gguf ./models 
cd models
ollama run mistral-7b-instruct-v0.1.Q5_K_M
```

## ElasticSearch db prep:

```sh
docker run -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.http.ssl.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.12.1
```

## Streamlit:

```sh
pip install streamlit

streamlit run ./model_gui/streamlit_app.py --server.port 8502
```