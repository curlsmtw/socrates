# SOCrates: AI-Driven SOC Assistant Design Document

## Overview
SOCrates is a beginner-friendly Security Operations Center (SOC) assistant. The goal is to use AI to help summarize logs, triage alerts, and suggest basic fixes for users with little security experience. The system is intended to be simple and modular so complexity can be added over time.

Important design constraints / clarifications (goals):
- This assistant is not intended to act as a multi-turn conversational chatbot. It will accept a single question (one-shot) and return an analysis based on available logs.
- Users do not upload logs as part of the interaction. The design assumes logs are already available in a configured repository or storage location accessible to SOCrates.

## Goals
- Summarize log files and alerts in plain language
- Help triage (prioritize) security alerts
- Suggest basic fixes or next steps
- Be easy to use for entry-level users
- Be modular and easy to expand

## High-Level Architecture
```
+-------------------+
|   FastAPI Server  |
+-------------------+
		 |
		 v
+-------------------+
|   API Endpoints   |
+-------------------+
		 |
		 v
+-------------------+
|   AI Assistant    |
+-------------------+
		 |
		 v
+-------------------+
| Log/Alert Loader  |
+-------------------+
		 |
		 v
+-------------------+
|  Vector Store     |
+-------------------+
		 |
		 v
+-------------------+
|   LLM Provider    |
+-------------------+
```

## Main Components (planned)

### 1. Document Loader - Using LangChain
- Load logs from a configured source (filesystem, archive, or ingestion pipeline). Note: user upload is not part of the primary interaction model.
- Convert logs into a document format the AI can consume
- Example: `src/document_loader.py`

### 2. Text Splitter
- Split large logs into smaller, manageable chunks
- Help the AI process information efficiently
- Example: `src/text_splitter.py`

### 3. Embedding Model
- Convert text chunks into numerical vectors
- Vectors help the AI search and understand context
- Example: `src/embedding_model.py`

### 4. Vector Store
- Store and retrieve vectorized log data
- Enable fast semantic search and retrieval for the assistant
- Example: `src/vector_store.py`

### 5. Prompt Template
- Define one-shot prompt templates that ask the LLM to summarize, triage, or suggest fixes in beginner-friendly language
- Example: `src/prompt_template.py`

### 6. Analysis Model (AI Assistant)
- Use LangChain and a selected LLM to analyze retrieved context and produce a single, actionable response per request
- The assistant will not maintain chat history or multi-turn state in the initial design
- Example: `src/chat_model.py`

### 7. FastAPI Interface
- Provide API endpoints for submitting a single question and returning an analysis
- Endpoints assume the service has access to pre-ingested/pre-existing logs and a populated vector store
- The API will return structured results (summary, triage rating, suggested next steps)

## Technology Choices
- **FastAPI**: For building the web API interface
- **LangChain**: For building the AI assistant and managing prompts
- **HuggingFace**: For using pre-trained language models (LLMs)
- **Python**: Main programming language

## Development steps (goals / roadmap)
1. Set up project structure and skeleton code
2. Implement Document Loader to read logs from configured sources
3. Add Text Splitter for large logs
4. Integrate an Embedding Model for vectorization
5. Set up a Vector Store for fast semantic search
6. Create one-shot Prompt Templates for clear, beginner-friendly requests
7. Build the Analysis Model using LangChain + selected LLMs
8. Set up FastAPI endpoints for submitting a single question and returning an analysis
   - Note: the initial API will not accept user log uploads; it will query logs already available to the system
9. Handle single-message interactions
   - Support only one question at a time; do not implement conversation history in the initial release
10. Test with sample logs and single questions
11. Add error handling and user-friendly responses
12. Document API usage and example requests
13. Iterate and add features (alert triage, dashboard, etc.)
14. (Future) Consider multi-turn conversation support and context retention once single-turn behavior is stable
## Example (one-shot) User Flow
1. Logs are assumed to be available to SOCrates via a configured source or ingestion pipeline (no user upload step).
2. A user submits a single question to the API (for example: "Did anything suspicious happen in the last hour?").
3. The service retrieves relevant log chunks from the vector store, runs a one-shot analysis with the LLM, and returns:
	- A brief plain-language summary
	- A triage/priority assessment (if applicable)
	- Suggested next steps or fixes
4. The response is a single, self-contained result. There is no conversation state retained between requests in this design.

## Tips for Beginners
- Start simple: focus on building the FastAPI endpoints for one-shot questions and summary responses (remember: no user upload in the initial model)
- Use clear, plain language in prompts and responses
- Add features gradually (alert triage, dashboard, etc.)
- Read FastAPI, LangChain, and HuggingFace documentation for examples

## Future Ideas
- Add alert prioritization and triage improvements
- Integrate with real-time log sources and ingestion pipelines
- Build a web dashboard (future)
- Add user authentication and role management
