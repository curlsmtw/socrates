from src.document_loader import DocumentLoader
from src.text_splitter import LineOverlapTextSplitter
from src.embedding_model import EmbeddingModel

if __name__ == "__main__":
    loader = DocumentLoader("example_logs")
    documents = loader.load_logs()

    splitter = LineOverlapTextSplitter(2, 1)
    chunks = []
    for doc in documents:
        chunks.extend(splitter.split(doc.page_content))

    embedding_model = EmbeddingModel()
    for chunk in chunks:
        embedding = embedding_model.embed_query(chunk)
        print(f"Chunk: {chunk}\nEmbedding: {embedding}\n")
