# RAG-QA-System

A RAG-based intelligent question answering system built with LangChain, Chroma, and Tongyi Qianwen.

## ✨ Features

- 📁 **Knowledge Base Management**: Upload TXT files for automatic vectorization and storage
- 🔍 **Intelligent Retrieval**: Document retrieval based on vector similarity
- 💬 **Conversation Memory**: Multi-turn dialogue support with context retention
- 🎨 **Web Interface**: User-friendly interface built with Streamlit
- 🗑️ **File Management**: View and delete uploaded files

## 🛠️ Tech Stack

- **Framework**: LangChain
- **Vector Database**: Chroma
- **Embedding Model**: Tongyi Qianwen text-embedding-v4
- **Chat Model**: Tongyi Qianwen qwen3-max
- **Web UI**: Streamlit

## 📁 Project Structure
├── app_file_uploader.py # File upload management interface
├── app_qa.py # Q&A interface
├── config_data.py # Configuration file
├── file_history_store.py # Chat history storage
├── knowledge_base.py # Knowledge base core logic
├── rag.py # RAG service
├── vector_stores.py # Vector storage service
├── requirements.txt # Dependencies
└── README.md # Documentation

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Luckrezia/RAG-QA-System.git
cd RAG-QA-System
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Set up API Key
```
# Linux/Mac
export DASHSCOPE_API_KEY="your-api-key"

# Windows
set DASHSCOPE_API_KEY="your-api-key"
```
### 4. Run the application
File Upload Interface:
```
streamlit run app_file_uploader.py
```

Q&A Interface:
```
streamlit run app_qa.py
```

### Configuration
Adjustable parameters in config_data.py:

chunk_size: Text chunk size (default: 1000)

chunk_overlap: Chunk overlap size (default: 100)

similarity_threshold: Similarity retrieval threshold

persist_directory: Vector database storage path


### Notes
Requires a valid Tongyi Qianwen API key
Vector database files are stored in ./chroma_db/
Chat history is stored in ./chat_history/
