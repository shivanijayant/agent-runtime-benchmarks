import pandas as pd
import json, time

start = time.time()
df = pd.read_csv('transactions.csv')
summary = df.groupby('category')['amount'].sum().reset_index()

with open('summary.md', 'w') as f:
    for _, row in summary.iterrows():
        f.write(f"- {row['category']}: ${row['amount']}\n")

print(json.dumps({"test": "baseline", "time_ms": (time.time() - start) * 1000}))
