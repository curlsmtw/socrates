class PromptTemplate:
    """
    PromptTemplate builds a single string prompt from system instructions,
    retrieved context, and a user query.

    Attributes:
            system_instructions (str): Top-level instructions to the model.

    Methods:
            format(context, user_query): Return a formatted prompt string.
    """

    def __init__(self, system_instructions: str = "You are a helpful assistant."):
        self.system_instructions = system_instructions

    def format(self, context, user_query: str) -> str:
        if isinstance(context, list):
            context_text = "\n\n".join([c for c in context if c])
        else:
            context_text = context or ""

        parts = [f"SYSTEM: {self.system_instructions}"]
        if context_text:
            parts.append(f"CONTEXT:\n{context_text}")
        parts.append(f"USER QUERY:\n{user_query}")
        return "\n\n".join(parts)
