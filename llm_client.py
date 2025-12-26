# llm_client.py
import time
from typing import Dict


class LLMResponse:
    """Standardized response object for all LLM calls."""

    def __init__(self, text: str, latency_ms: float, tokens: int, cost: float):
        self.text = text
        self.latency_ms = latency_ms
        self.tokens = tokens
        self.cost = cost


class BaseLLM:
    """Abstract interface for an LLM."""

    def generate(self, prompt: str) -> LLMResponse:
        raise NotImplementedError("LLM must implement generate()")


class MockLLM(BaseLLM):
    """
    Mock LLM used for local testing and development.
    Simulates latency, token usage, and deterministic output.
    """

    def __init__(self, model_name: str = "mock-llm"):
        self.model_name = model_name

    def generate(self, prompt: str) -> LLMResponse:
        start_time = time.time()

        # Simulate computation delay
        time.sleep(0.3)

        # Simple deterministic "generation"
        output = f"[{self.model_name} response] {prompt[::-1]}"

        latency_ms = (time.time() - start_time) * 1000

        # Rough token estimate: words * 1.3
        tokens = int(len(prompt.split()) * 1.3)

        # Mock cost model (free/local)
        cost = 0.0

        return LLMResponse(
            text=output,
            latency_ms=latency_ms,
            tokens=tokens,
            cost=cost,
        )


def get_llm(model_name: str) -> BaseLLM:
    """
    Factory method for retrieving an LLM instance.
    """
    registry: Dict[str, BaseLLM] = {
        "mock": MockLLM(),
    }

    if model_name not in registry:
        raise ValueError(f"Model '{model_name}' not supported.")

    return registry[model_name]

