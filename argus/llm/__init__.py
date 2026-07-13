"""LLM abstraction: swap backends without touching skill logic."""

from .base import LLMClient, LLMResult
from .ollama_client import OllamaClient

__all__ = ["LLMClient", "LLMResult", "OllamaClient"]
