# app.py
import streamlit as st
import requests
import pandas as pd

from evaluator import load_runs_df, model_summary, win_rate

API_URL = "http://127.0.0.1:8000"


st.set_page_config(page_title="LLM Evaluation Playground", layout="wide")

st.title("🧪 LLM Evaluation Playground")

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.header("Run Configuration")

prompt = st.sidebar.text_area("Prompt", height=120)

mode = st.sidebar.radio(
    "Mode",
    ["Single Model", "Side-by-Side Comparison"]
)

model_a = st.sidebar.selectbox("Model A", ["mock"])
model_b = None

if mode == "Side-by-Side Comparison":
    model_b = st.sidebar.selectbox("Model B", ["mock"], index=0)

run_button = st.sidebar.button("Run")

# -------------------------------
# Helper function
# -------------------------------
def run_model(prompt: str, model: str):
    response = requests.post(
        f"{API_URL}/generate",
        json={"prompt": prompt, "model": model},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


# -------------------------------
# Run Inference
# -------------------------------
if run_button and prompt.strip():
    st.subheader("🔍 Model Outputs")

    if mode == "Single Model":
        result = run_model(prompt, model_a)

        st.markdown(f"### {model_a}")
        st.write(result["output"])

        st.caption(
            f"Latency: {result['latency_ms']:.1f} ms | "
            f"Tokens: {result['tokens']} | "
            f"Cost: ${result['cost']:.4f}"
        )

        rating = st.slider(
            "Rate this output (1 = poor, 5 = excellent)",
            min_value=1,
            max_value=5,
            key="rating_single",
        )

        st.info("Rating is stored automatically with the run.")

    else:
        col1, col2 = st.columns(2)

        with col1:
            res_a = run_model(prompt, model_a)
            st.markdown(f"### {model_a}")
            st.write(res_a["output"])
            rating_a = st.slider(
                "Rating",
                1,
                5,
                key="rating_a"
            )

        with col2:
            res_b = run_model(prompt, model_b)
            st.markdown(f"### {model_b}")
            st.write(res_b["output"])
            rating_b = st.slider(
                "Rating",
                1,
                5,
                key="rating_b"
            )

        st.caption("Ratings are stored for evaluation.")

# -------------------------------
# Evaluation Dashboard
# -------------------------------
st.divider()
st.subheader("📊 Evaluation Metrics")

df = load_runs_df()

if df.empty:
    st.warning("No runs logged yet.")
else:
    summary_df = model_summary(df)
    st.dataframe(summary_df, use_container_width=True)

    st.subheader("🏆 Win Rates")
    wins = win_rate(df)

    if wins:
        st.bar_chart(pd.Series(wins))
    else:
        st.info("Not enough rated runs to compute win rates.")
