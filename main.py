from dotenv import load_dotenv

load_dotenv()

from src.document_loader import DocumentLoader
from src.text_splitter import LineOverlapTextSplitter
from src.embedding_model import EmbeddingModel
from src.vector_store import VectorStore
from src.chat_model import ChatModel
from src.prompt_template import PromptTemplate

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

    query = "Summarize the main topic of these logs."
    results = vector_store.similarity_search(query, k=3)
    print("Top matches from vector store:")
    context = [r.page_content for r in results]
    for r in results:
        print(f"- {r.page_content[:200]!r} ...")

    chat = ChatModel()
    prompt_t = PromptTemplate(
        system_instructions="You are a concise helpful assistant."
    )
    prompt = prompt_t.format(context, query)
    response = chat.invoke(prompt)
    print(f"Chat model response: {response}")
