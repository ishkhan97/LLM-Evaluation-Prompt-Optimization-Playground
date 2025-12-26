# evaluator.py
import pandas as pd
from typing import Dict

from db import fetch_runs


COLUMNS = [
    "id",
    "prompt",
    "model",
    "output",
    "latency_ms",
    "tokens",
    "cost",
    "rating",
    "created_at",
]


def load_runs_df(limit: int = 500) -> pd.DataFrame:
    """
    Load recent LLM runs into a pandas DataFrame.
    """
    rows = fetch_runs(limit=limit)
    df = pd.DataFrame(rows, columns=COLUMNS)

    # Ensure correct dtypes
    df["latency_ms"] = pd.to_numeric(df["latency_ms"], errors="coerce")
    df["tokens"] = pd.to_numeric(df["tokens"], errors="coerce")
    df["cost"] = pd.to_numeric(df["cost"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    return df


def model_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate metrics by model.
    """
    summary = (
        df.groupby("model")
        .agg(
            runs=("id", "count"),
            avg_latency_ms=("latency_ms", "mean"),
            avg_tokens=("tokens", "mean"),
            avg_cost=("cost", "mean"),
            avg_rating=("rating", "mean"),
        )
        .reset_index()
    )

    return summary.sort_values(by="avg_rating", ascending=False)


def cost_quality_tradeoff(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return cost vs quality metrics for visualization.
    """
    return (
        df.groupby("model")
        .agg(
            avg_cost=("cost", "mean"),
            avg_rating=("rating", "mean"),
        )
        .reset_index()
    )


def win_rate(df: pd.DataFrame) -> Dict[str, float]:
    """
    Compute win rate per model based on highest rating per prompt.
    """
    wins = {}

    # Group by prompt to compare models on same task
    for _, group in df.dropna(subset=["rating"]).groupby("prompt"):
        best_rating = group["rating"].max()
        winners = group[group["rating"] == best_rating]["model"]

        for model in winners:
            wins[model] = wins.get(model, 0) + 1

    total = sum(wins.values())
    return {model: count / total for model, count in wins.items()}
