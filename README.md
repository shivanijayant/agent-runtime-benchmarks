# AI Agent Runtime Benchmarks: E2B Sandbox vs. AWS Bedrock AgentCore

Generating code with an LLM is a solved problem. Safely executing that untrusted, dynamically generated code in production is an ongoing infrastructure challenge. 

This repository contains a head-to-head benchmarking suite designed to test how modern cloud environments handle the unpredictable nature of AI agent workloads. It compares two fundamentally different architectures: **E2B** (Firecracker microVMs) and **AWS Bedrock AgentCore** (Serverless execution).

## The Architectures Tested

1. **E2B Sandbox (Code-First):** Dynamically provisioned, isolated Linux microVMs that behave like a standard OS.
2. **AWS Bedrock AgentCore (Infrastructure-First):** Fully managed, serverless compute environments triggered via API invocation.

## The Benchmark Suite

The `agents/` directory contains three tests designed to push the boundaries of an AI execution environment:

* **`01_baseline.py` (Speed & Dependencies):** Reads a CSV, aggregates data, and writes a markdown summary. Tests how fast the environment boots and how it handles heavy external libraries (like `pandas`) vs. native modules.
* **`02_stress_test.py` (Guardrails):** Intentionally hoards 1GB of RAM and maxes out the CPU. Tests if the infrastructure protects the host environment by killing the process, or if it absorbs the spike.
* **`03_state_test.py` (State Persistence):** Writes a unique UUID to a file, exits, and attempts to read it in a subsequent invocation. Tests ephemeral storage behavior and filesystem permissions.

## Key Findings & Architectural Tradeoffs

### 1. Cold Starts and Dependency Bloat
* **E2B:** Handled heavy data science libraries flawlessly. Installing `pandas` dynamically worked as expected, and the microVM booted in **0.20 seconds**.
* **AWS:** Pushing a 100MB+ `pandas` deployment package caused severe CPU bottlenecks during the serverless cold start, resulting in consistent 30-second initialization timeouts. 
* **The Fix:** Rewriting the AWS script to use Python's native `csv` module dropped the package size to 0.00 MB, resulting in a blistering **0.12 millisecond** execution time on a warm start.

### 2. Hardware and Cross-Compilation
Developing locally on Apple Silicon (M1) requires careful dependency management. To bypass building heavy Docker containers for AWS, this project leverages `uv` to actively cross-compile packages to the Linux ARM64 architecture required by the Bedrock AgentCore runtime.

### 3. File System Constraints
* **E2B:** Provides a fully writable filesystem running as root.
* **AWS:** Enforces a strictly read-only main filesystem (`/var/task/`). Code must be explicitly routed to write to `/tmp/`, which is the only writable directory in the serverless environment.

### 4. Infrastructure Guardrails
When the `02_stress_test.py` script attempted to consume 1GB of memory:
* **E2B** immediately intercepted the greedy process and returned a `"status": "memory_killed"` exception to protect the sandbox.
* **AWS AgentCore**'s default compute tier successfully absorbed the massive memory spike without crashing, returning a `"survived"` status.

## Project Structure

```text
├── agents/
│   ├── 01_baseline.py      # Latency & dependency test
│   ├── 02_stress_test.py   # 1GB memory bloat guardrail test
│   └── 03_state_test.py    # Ephemeral memory /tmp/ test
├── e2b_runner/
│   └── run_suite.py        # Code to provision and test E2B microVMs
├── agentcore_runner/
│   └── app.py              # AWS Bedrock entrypoint and routing logic
├── data/
│   └── transactions.csv    # Sample dataset for baseline test
├── .gitignore
└── README.md

## How to Run

### E2B Testing
> **Note:** Requires an active E2B API key configured in your environment.

```bash
python e2b_runner/run_suite.py

### AWS Bedrock AgentCore Testing
> **Note: Requires AWS CLI credentials configured locally with AdministratorAccess (or strictly scoped Bedrock/IAM/S3 policies).

```bash
cd agentcore_runner
agentcore deploy
agentcore invoke '{"test": "baseline"}'
agentcore invoke '{"test": "stress"}'
agentcore invoke '{"test": "state_write"}'
agentcore invoke '{"test": "state_read"}'
