# LLM-Evaluation-Prompt-Optimization-Playground
This project is a small, production-style web application for collecting, evaluating, and analyzing generated text responses. It provides a simple API for submitting requests, a lightweight UI for reviewing outputs, and a data layer for storing results and human feedback. The system is designed to be modular, observable, and easy to extend as requirements evolve.

This folder includes test files too. 

## Features
- Run prompts across multiple LLMs
- Log latency, token usage, and estimated cost
- Side-by-side output comparison
- Human-in-the-loop quality ratings
- Simple analytics for model and prompt selection

## Tech Stack
- Backend: Python, FastAPI (async APIs, request handling)
- Frontend: Streamlit (lightweight UI for review and feedback)
- Data Processing: Pandas (aggregation, analysis, metrics)
- Serving: Uvicorn (local development server)
- Architecture: Modular services with clear separation  between API, data, and presentation layers

## Key Learnings
- Prompt engineering as experimentation
- Practical LLM evaluation strategies
- Tradeoffs between quality, cost, and latency
- Building simple ML evaluation infrastructure

## Future Work
- Automatic evaluation using LLM-as-a-judge
- Retrieval-Augmented Generation (RAG)
- Support for local inference (vLLM)

Thanks!
