from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from importlib import import_module
import logging
from contextlib import asynccontextmanager
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger("uvicorn.error")
    try:
        mod = import_module("src.rag_modules.main")
        RAGPipeline = getattr(mod, "RAGPipeline")
        pipeline = RAGPipeline()
        try:
            await asyncio.to_thread(pipeline.build_retrieval)
            logger.info("RAG pipeline initialized and vector store built at startup.")
        except Exception as build_err:
            logger.warning(
                "RAG pipeline created but build_retrieval failed at startup: %s",
                build_err,
            )
        app.state.rag_pipeline = pipeline
    except Exception as e:
        logger = logging.getLogger("uvicorn.error")
        logger.exception("Failed to import/initialize RAG pipeline: %s", e)
        app.state.rag_pipeline = None
    try:
        yield
    finally:
        pass


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/rag_query")
def rag_query(q: Optional[str] = None, k: int = 3):
    if not q:
        return {"error": "missing query parameter 'q'"}
    pipeline = getattr(app.state, "rag_pipeline", None)
    if pipeline is None:
        return {
            "query": q,
            "error": "RAG pipeline unavailable",
            "details": "pipeline not initialized",
            "fallback": f"Echo: {q}",
        }
    try:
        results, context = pipeline.retrieve(q, k=k)
        response = pipeline.generate_response(context, q)
        return {"query": q, "response": response, "context": context}
    except Exception as e:
        logging.getLogger("uvicorn.error").exception("Error during /rag_query: %s", e)
        return {
            "query": q,
            "error": "RAG pipeline error",
            "details": str(e),
            "fallback": f"Echo: {q}",
        }
