# Video SDK RAG Agent

This project implements a Retrieval-Augmented Generation (RAG) voice assistant using the Video SDK. The agent can answer questions based on a knowledge base of documents, and falls back to its own knowledge when no relevant information is found in the documents.

## Features

- **Voice-based interaction**: The agent uses Speech-to-Text (STT) and Text-to-Speech (TTS) to communicate with the user.
- **RAG pipeline**: The agent uses a RAG pipeline to retrieve relevant information from a knowledge base and generate answers.
- **Document ingestion**: The project includes a script to ingest documents into the knowledge base.
- **Multiple document formats**: The document loader supports various formats, including PDF, DOCX, TXT, and more.
- **ChromaDB vector store**: The project uses ChromaDB to store and query document embeddings.
- **Gemini embeddings**: The project uses the Gemini API to generate document embeddings.

## Project Structure

```
video_sdk_assignment/
├── .env
├── agent.py
├── main.py
├── pipeline.py
├── rag_conversational_flow.py
├── requirements.txt
├── docs/
└── utils/
    ├── agent_utils/
    │   └── agent_instruction.py
    └── helpers/
        ├── chroma_db.py
        ├── chunking_method.py
        ├── document_loader.py
        ├── gemini_embedding.py
        └── rag_handler.py
```

- **`main.py`**: The entry point of the application. It handles document ingestion and starting the RAG agent.
- **`agent.py`**: Defines the `RAGAgent` class, which is the core of the voice assistant.
- **`pipeline.py`**: Sets up the RAG pipeline, including STT, LLM, TTS, and other components.
- **`rag_conversational_flow.py`**: Defines the conversation logic for the RAG agent.
- **`requirements.txt`**: Lists the Python dependencies for the project.
- **`.env`**: Contains environment variables, including API keys and configuration for ChromaDB and RAG.
- **`docs/`**: A directory to store the documents for the knowledge base.
- **`utils/`**: Contains helper modules for various tasks, such as document loading, chunking, and RAG handling.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/video_sdk_assignment.git
   cd video_sdk_assignment
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the environment variables:**
   - Create a `.env` file in the root of the project.
   - Add the following environment variables to the `.env` file:
     ```
     VIDEOSDK_AUTH_TOKEN=<your_videosdk_auth_token>
     VIDSDK_JWT_TOKEN=<your_videosdk_jwt_token>
     GOOGLE_API_KEY=<your_google_api_key>
     SARVAMAI_API_KEY=<your_sarvamai_api_key>
     ```

## Usage

1. **Ingest documents:**
   - Place the documents you want to use for the knowledge base in the `docs/` directory.
   - Run the `main.py` script to ingest the documents:
     ```bash
     python main.py
     ```
   - The script will prompt you to enter the path to the directory to ingest. Enter `docs` to ingest the documents in the `docs/` directory.

2. **Start the RAG agent:**
   - After the document ingestion is complete, the script will automatically start the RAG agent.
   - The agent will be available to answer questions based on the knowledge base.

## Dependencies

The project uses the following dependencies:

- `requests`
- `videosdk-plugins-google`
- `videosdk-plugins-silero`
- `videosdk-plugins-turn_detector`
- `videosdk-plugins-sarvamai`
- `google-genai`
- `chromadb`

You can install all the dependencies by running `pip install -r requirements.txt`.

## Example Queries and Expected behaviors  

**Question 1**: Can you tell me about the the author's grand-mother?

**Expected answer**: The Answer should be from the file hornbill-1-20.pdf as in the first chapter it's shown and the agent should retrieve the document accordingly and decribe the author's grand-mother.

**Question 2**: What is Quantum physics?

**Expected answer**: The Answer should be provided the LLM it self with out using any context as it will be baked into the knowledge base of the LLM Agent

