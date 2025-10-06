from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint


class ChatModel:
    """
    ChatModel wraps a Hugging Face LLM endpoint and exposes a simple
    invoke method to generate text.

    Attributes:
        llm: The Hugging Face endpoint configuration object.
        chat_model: The `ChatHuggingFace` instance used to generate text.

    Methods:
        invoke(prompt): Send `prompt` to the model and return its response.
    """

    def __init__(self):
        self.llm = HuggingFaceEndpoint(
            repo_id="deepseek-ai/DeepSeek-R1-0528",
            task="text-generation",
            max_new_tokens=512,
            temperature=0.0,
            repetition_penalty=1.0,
        )
        self.chat_model = ChatHuggingFace(llm=self.llm)

    def invoke(self, prompt: str):

        return self.chat_model.invoke(prompt)
