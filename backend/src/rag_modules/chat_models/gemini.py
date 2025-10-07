from langchain_google_genai import ChatGoogleGenerativeAI


class ChatModel:
    """
    ChatModel wraps a Google Gemini LLM and exposes a simple
    invoke method to generate text.

    Attributes:
        llm: The Gemini LLM configuration object.
        chat_model: The `ChatGoogleGenerativeAI` instance used to generate text.

    Methods:
        invoke(prompt): Send `prompt` to the model and return its response.
    """

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        self.chat_model = self.llm

    def invoke(self, prompt: str):
        return self.chat_model.invoke(prompt)
