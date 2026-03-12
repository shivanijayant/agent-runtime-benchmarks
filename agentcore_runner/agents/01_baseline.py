import csv, json, time
from collections import defaultdict

start = time.time()
summary = defaultdict(float)

# Read CSV using built-in library
with open('data/transactions.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        summary[row['category']] += float(row['amount'])

# Write report
with open('/tmp/summary.md', 'w') as f:
    f.write("# Financial Summary\n\n")
    for category, amount in summary.items():
        f.write(f"- **{category}**: ${amount:.2f}\n")

print(json.dumps({"test": "baseline", "time_ms": (time.time() - start) * 1000}))
