from llm_client import get_llm

llm = get_llm("mock")

response = llm.generate("Explain LLM evaluation")

print("Output:", response.text)
print("Latency (ms):", response.latency_ms)
print("Tokens:", response.tokens)
print("Cost:", response.cost)
