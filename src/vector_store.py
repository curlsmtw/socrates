from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List, Optional, Union


class VectorStore:
    """
    VectorStore is a minimal class wrapper around a Chroma vector store.

    This class replaces the previous module-level helper functions and
    provides a simple, class-based API.

    Attributes:
        client: The underlying `Chroma` instance.

    Methods:
        add_documents(documents, ids=None): Add documents (or string chunks)
            to the collection and return the added IDs.
    """

    def __init__(
        self,
        embedding_function,
        collection_name: str = "example_collection",
        persist_directory: str = "./chroma_langchain_db",
    ):
        self.client = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_function,
            persist_directory=persist_directory,
        )

    def add_documents(
        self,
        documents: Union[List[Document], List[str]],
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        if documents and isinstance(documents[0], str):
            documents = [Document(page_content=chunk) for chunk in documents]
        return self.client.add_documents(documents=documents, ids=ids)
