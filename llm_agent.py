"""
Optional LLM helpers. Safe to import even without API keys.

Usage is gated by env vars:
  ENABLE_LLM=1 and OPENAI_API_KEY set → attempts LLM calls
Otherwise returns None and the caller should fallback.
"""

import os
from typing import Optional, Dict, Any


def is_llm_enabled() -> bool:
    return os.getenv("ENABLE_LLM", "0") == "1" and bool(os.getenv("OPENAI_API_KEY"))


def generate_text(prompt: str, system: Optional[str] = None, model: str = "gpt-4o-mini", **kwargs) -> Optional[str]:
    """Generate text via LLM if enabled; otherwise return None.
    This function avoids importing SDKs to keep runtime lightweight.
    """
    if not is_llm_enabled():
        return None

    # Placeholder: integrate your preferred LLM client here.
    # For safety, we no-op unless a concrete client is wired.
    # Example (pseudo):
    #   import openai
    #   openai.api_key = os.environ['OPENAI_API_KEY']
    #   resp = openai.chat.completions.create(model=model, ...)
    #   return resp.choices[0].message.content

    # Until wired, return None so callers can fallback cleanly
    return None


