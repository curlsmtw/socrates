from src.document_loader import DocumentLoader
from src.text_splitter import LineOverlapTextSplitter
from src.embedding_model import EmbeddingModel
from src.vector_store import VectorStore

if __name__ == "__main__":
    loader = DocumentLoader("example_logs")
    documents = loader.load_logs()

    splitter = LineOverlapTextSplitter(2, 1)
    chunks = []
    for doc in documents:
        chunks.extend(splitter.split(doc.page_content))

    embedding = EmbeddingModel()
    vector_store = VectorStore(
        embedding_function=embedding.model, collection_name="log_collection"
    )
    vector_store.add_documents(chunks)
    print(f"Added {len(chunks)} chunks to the vector store.")
