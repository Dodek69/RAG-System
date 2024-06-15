# RAG-System
This project showcases the implementation of a Retrieval-Augmented Generation (RAG) system, combining the power of a vector database and a language model to enhance information retrieval and generation capabilities.


## Model prep:
Install ollama from https://ollama.com/download or by running
`curl -fsSL https://ollama.com/install.sh | sh` on Linux.

Download `Mistral-7B-Instruct-v0.3.Q8_0.gguf` model from https://huggingface.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF/tree/main and run commands below to create Ollama model:

```sh
cp Mistral-7B-Instruct-v0.3.Q8_0.gguf ./models 
ollama create Mistral-7B-Instruct-v0.3.Q8_0.gguf -f ./models/Mistral-7B-Instruct-v0.3.Q8_0.gguf
```

## ElasticSearch db prep:
```sh
docker-compose up
```

## Install dependencies
```sh
pip install langchain-elasticsearch langchain-community tqdm pypdf streamlit langchain-experimental
```

## Run Streamlit GUI:
```sh
streamlit run streamlit_app.py --server.enableXsrfProtection false --server.port 8540
```
