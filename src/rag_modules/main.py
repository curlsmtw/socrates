from dotenv import load_dotenv

load_dotenv()

from src.rag_modules.document_loader import DocumentLoader
from src.rag_modules.text_splitter import LineOverlapTextSplitter
from src.rag_modules.embedding_model import EmbeddingModel
from src.rag_modules.vector_store import VectorStore
from src.rag_modules.prompt_template import PromptTemplate
from src.rag_modules.chat_models.main import ChatModelSelector


class RAGPipeline:
    """
    RAGPipeline is a class for building and querying a retrieval-augmented
    generation (RAG) pipeline from a folder of documents.

    Attributes:
        persist_directory (str): Path to the vector store persistence directory.
        collection_name (str): Name of the vector store collection.
        loader_path (str): Path to the folder containing documents to ingest.
        splitter_args (tuple): Arguments passed to the text splitter.

    Methods:
        build_retrieval():
            Loads documents from `loader_path`, splits them, builds embeddings,
            creates/initializes the vector store at `persist_directory`, and
            returns the VectorStore instance.
        retrieve(query, k=3):
            Runs a similarity search against the vector store and returns a
            tuple `(results, context)` where `context` is a list of page
            contents extracted from the top matches.
        generate_response(context, query, system_instructions=...):
            Formats a prompt from `context` and `query` using
            `PromptTemplate` and invokes the `ChatModel` to produce a
            response string.
    """

    def __init__(
        self,
        persist_directory: str = "chroma_langchain_db",
        collection_name: str = "log_collection",
        loader_path: str = "example_logs",
        splitter_args=(2, 1),
        model_backend: str | None = None,
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.loader_path = loader_path
        self.splitter_args = splitter_args
        self.vector_store = None
        self.model_backend = model_backend
        self.chat_selector = ChatModelSelector()

    def build_retrieval(self):

        loader = DocumentLoader(self.loader_path)
        documents = loader.load_logs()

        splitter = LineOverlapTextSplitter(*self.splitter_args)
        chunks = []
        for doc in documents:
            chunks.extend(splitter.split(doc.page_content))

        embedding = EmbeddingModel()
        self.vector_store = VectorStore(
            embedding_function=embedding.model,
            collection_name=self.collection_name,
            persist_directory=self.persist_directory,
        )
        self.vector_store.add_documents(chunks)
        return self.vector_store

    def retrieve(self, query: str, k: int = 3):
        if self.vector_store is None:
            self.build_retrieval()
        results = self.vector_store.similarity_search(query, k=k)
        context = [r.page_content for r in results]
        return results, context

    def generate_response(
        self,
        context,
        query,
        system_instructions: str = "You are a concise helpful assistant.",
    ):
        chat = self.chat_selector.get_chat_model(self.model_backend)
        prompt_t = PromptTemplate(system_instructions=system_instructions)
        prompt = prompt_t.format(context, query)
        response = chat.invoke(prompt)
        return response
