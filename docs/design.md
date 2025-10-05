# SOCrates: AI-Driven SOC Assistant Design Document

## Overview
SOCrates is a beginner-friendly Security Operations Center (SOC) assistant. It uses AI to help summarize logs, triage alerts, and suggest fixes for users with little security experience. The system is designed to be simple and modular, so you can add complexity over time.

**For now, SOCrates is a web API application built with FastAPI. Users interact with it by uploading `.txt` log files through the API.**

## Goals
- Summarize log files and alerts in plain language
- Help triage (prioritize) security alerts
- Suggest basic fixes or next steps
- Easy to use for entry-level users
- Modular and easy to expand

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

## Main Components

### 1. Document Loader
- Loads log files (.txt, .log) from a directory
- Converts them into a format the AI can understand
- Example: `src/document_loader.py`

### 2. Text Splitter
- Splits large logs into smaller, manageable chunks
- Helps the AI process information efficiently
- Example: `src/text_splitter.py`

### 3. Embedding Model
- Converts text chunks into numerical vectors
- Vectors help the AI search and understand context
- Example: `src/embedding_model.py`

### 4. Vector Store
- Stores and retrieves vectorized log data
- Enables fast search and retrieval for the AI
- Example: `src/vector_store.py`

### 5. Prompt Template
- Defines how questions and summaries are asked to the AI
- Ensures clear, beginner-friendly language
- Example: `src/prompt_template.py`

### 6. Chat Model (AI Assistant)
- Uses LangChain and HuggingFace LLMs
- Answers user questions, summarizes logs, suggests fixes
- Example: `src/chat_model.py`

### 7. FastAPI Interface
- Users interact with SOCrates through a web API (FastAPI)
- Users upload `.txt` log files via API endpoints
- The assistant processes these files and provides summaries, triage, and suggestions through API responses

## Technology Choices
- **FastAPI**: For building the web API interface
- **LangChain**: For building the AI assistant and managing prompts
- **HuggingFace**: For using pre-trained language models (LLMs)
- **Python**: Main programming language

## Development Steps
1. **Set up project structure** (done)
2. **Implement Document Loader** to read logs
3. **Add Text Splitter** for large files
4. **Integrate Embedding Model** for vectorization
5. **Set up Vector Store** for fast search
6. **Create Prompt Templates** for clear communication
7. **Build Chat Model** using LangChain + HuggingFace
8. **Set up FastAPI endpoints** for:
	- Uploading log files
	- Sending a single message/question to the assistant
9. **Handle single-message interactions**
	- For now, only support one question at a time (no conversation history)
	- Return a summary, triage, or suggestion based on the uploaded logs and the user's message
10. **Test with sample logs and single questions**
11. **Add error handling and user-friendly responses**
12. **Document API usage and example requests**
13. **Iterate and add features** (alert triage, dashboard, etc.)
14. **(Future) Add conversation flow support**
	- Enable multi-turn conversations and context retention

## Example User Flow
1. User uploads `.txt` log files using the FastAPI endpoint
2. SOCrates loads and summarizes logs
3. User sends questions to the API (e.g., "What happened in the last hour?")
4. Assistant provides simple, actionable answers in the API response
5. Assistant suggests basic fixes or next steps

## Tips for Beginners
- Start simple: focus on building the FastAPI endpoints for log upload and summary
- Use clear, plain language in prompts and responses
- Add features gradually (alert triage, dashboard, etc.)
- Read FastAPI, LangChain, and HuggingFace documentation for examples

## Future Ideas
- Add alert prioritization and triage
- Integrate with real-time log sources
- Build a web dashboard (future)
- Add user authentication and role management

---
This document is a starting point. As you learn more, you can expand and improve SOCrates over time.
