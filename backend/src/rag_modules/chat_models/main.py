"""Chat model selector utilities.

This module provides ChatModelSelector, a small helper for selecting and
loading chat model backends that live under the `src.rag_modules.chat_models`
package. The selector centralizes backend resolution (explicit name,
environment variable, or default) and handles safe fallback to a
default backend.

Example:
    selector = ChatModelSelector()
    ChatModelClass = selector.get_chat_model_class("gemini")
    chat = ChatModelClass()

"""

import os
from importlib import import_module
from typing import Type


class ChatModelSelector:
    """
    ChatModelSelector is a helper class for selecting and loading chat model
    backends from the `src.rag_modules.chat_models` package.

    Attributes:
        default_backend (str): The fallback backend name to use when none is
            provided and the `CHAT_MODEL` environment variable is not set.

    Methods:
        _resolve_backend_name(name): Resolve the backend name using the
            explicit `name`, then the `CHAT_MODEL` env var, then the default.
        get_chat_model_class(name=None): Import and return the `ChatModel`
            class from the selected backend module. Falls back to the
            `huggingface` backend if the requested module can't be imported.
        get_chat_model(name=None): Instantiate and return a `ChatModel`
            instance from the selected backend.
    """

    def __init__(self, default_backend: str = "huggingface"):
        self.default_backend = default_backend

    def _resolve_backend_name(self, name: str | None) -> str:
        if name:
            return name.lower()
        return os.getenv("CHAT_MODEL", self.default_backend).lower()

    def get_chat_model_class(self, name: str | None = None) -> Type:
        backend = self._resolve_backend_name(name)
        try:
            mod = import_module(f"src.rag_modules.chat_models.{backend}")
            return getattr(mod, "ChatModel")
        except Exception:
            mod = import_module("src.rag_modules.chat_models.huggingface")
            return getattr(mod, "ChatModel")

    def get_chat_model(self, name: str | None = None):
        cls = self.get_chat_model_class(name)
        return cls()
