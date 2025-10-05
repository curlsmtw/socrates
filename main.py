from src.document_loader import DocumentLoader
from src.text_splitter import LineOverlapTextSplitter

if __name__ == "__main__":
    loader = DocumentLoader("example_logs")
    documents = loader.load_logs()

    splitter = LineOverlapTextSplitter(2, 1)
    for doc in documents:
        chunks = splitter.split(doc.page_content)
        print(chunks)
