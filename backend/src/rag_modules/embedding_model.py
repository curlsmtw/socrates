from langchain_huggingface import HuggingFaceEmbeddings


class EmbeddingModel:
    """
    EmbeddingModel is a thin wrapper around a Hugging Face embeddings model
    provided by `langchain_huggingface`.

    Attributes:
            model_name (str): Hugging Face model identifier used to instantiate
                    the embeddings model. Defaults to
                    "sentence-transformers/all-mpnet-base-v2".
            model: The instantiated `HuggingFaceEmbeddings` object.

    Methods:
            embed_query(text): Compute embedding vector(s) for the provided text.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        self.model_name = model_name
        self.model = HuggingFaceEmbeddings(model_name=model_name)

    def embed_query(self, text: str):
        return self.model.embed_query(text)
