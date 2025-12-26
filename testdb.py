from db import init_db, insert_run, fetch_runs

init_db()

insert_run(
    prompt="Explain reinforcement learning simply.",
    model="gpt-4",
    output="Reinforcement learning is...",
    latency_ms=1200,
    tokens=150,
    cost=0.004,
    rating=4,
)

print(fetch_runs())
