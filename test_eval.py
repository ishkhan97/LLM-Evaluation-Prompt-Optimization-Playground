from evaluator import load_runs_df, model_summary, win_rate

df = load_runs_df()

print("=== Summary ===")
print(model_summary(df))

print("\n=== Win Rates ===")
print(win_rate(df))
