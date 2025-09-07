from src.document_loader import DocumentLoader

if __name__ == "__main__":
    loader = DocumentLoader("logs")
    documents = loader.load_logs()
    print(documents)
