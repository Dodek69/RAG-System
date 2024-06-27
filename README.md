# RAG-System
This project showcases the implementation of a Retrieval-Augmented Generation (RAG) system, combining the power of a vector database and a language model to enhance information retrieval and generation capabilities.


## Model prep:
Install ollama from https://ollama.com/download or by running
`curl -fsSL https://ollama.com/install.sh | sh` on Linux.

Download `Lexi-Llama-3-8B-Uncensored_Q8_0.gguf` model from https://huggingface.co/Orenguteng/Llama-3-8B-Lexi-Uncensored-GGUF/tree/main to ./models directory and then run command below to create Ollama model:
```sh
ollama create Lexi-Llama-3-8B-Uncensored_Q8_0.gguf -f ./models/Lexi-Llama-3-8B-Uncensored_Q8_0.gguf
```

## ElasticSearch db prep:
```sh
docker-compose up
```

## Install dependencies
```sh
pip install langchain-elasticsearch langchain-community tqdm pypdf streamlit langchain-experimental
```

```sh
pip install fastembed

# or with GPU support

pip install fastembed-gpu
```

## Run Streamlit GUI:
```sh
streamlit run streamlit_app.py --server.enableXsrfProtection false --server.port 8540
```
