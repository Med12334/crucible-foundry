# Crucible-Foundry — 36-Layer Frontier AI Code Evaluation Benchmark, Python AST & Control-Flow Graph (CFG) Static Verifier, Adversarial Differential Fuzzer, Unbiased Pass@k Stream Conduit & Polyglot Sandbox Jail

Crucible-Foundry is a 36-layer polyglot software engineering and AI evaluation platform designed to benchmark frontier language models on algorithmic reasoning, bug repair, edge-case resilience, execution efficiency, and code quality across Python, Rust, Go, C++20, and TypeScript.

## 36-Layer Polyglot Architecture Matrix

| Layers | Module Directory | Language / Stack | Core AI Code Evaluation Capabilities |
| :--- | :--- | :--- | :--- |
| **Layers 1–7** | `py-ast-cfg-analyzer` | **Python 3.11 (`ast`, `pytest`)** | Real `ast.NodeVisitor` static analyzer computing McCabe cyclomatic complexity, nested loop Big-$O$ depth, type-annotation coverage, infinite-loop traps, and forbidden sandbox-escape imports (`subprocess`, `eval`, `ctypes`). |
| **Layers 8–14** | `py-crucible-benchmark-deck` | **Python 3.11 (`FastAPI`, `pytest`)** | Differential benchmark harness comparing AI-generated candidate functions against ground-truth reference oracles across adversarial boundary cases (empty sets, zero-length intervals, 64-bit extremes). |
| **Layers 15–20** | `go-eval-stream-conduit` | **Go 1.22 (`go test`)** | High-throughput evaluation pipeline with SHA-256 whitespace-normalized completion deduplication and exact unbiased Chen et al. $\text{Pass}@k$ combinatorial estimation. |
| **Layers 21–26** | `rust-sandbox-jailer` | **Rust (Edition 2021)** | Memory-safe polyglot execution warden enforcing wall-clock timeout traps, RSS memory quotas, and mutation-testing kill-ratio scoring. |
| **Layers 27–31** | `cpp20-reference-oracle` | **C++20 (`g++ -O3`)** | Sub-microsecond ground-truth reference solver implementing $O(V + E)$ Kahn topological cycle detection and $O(N \times M)$ Levenshtein patch edit distance. |
| **Layers 32–36** | `ts-leaderboard-console` & `.github/workflows` | **TypeScript, React 18, Node 20, GitHub Actions** | Composite frontier leaderboard ranker and **7-job parallel CI matrix** verifying every language and test suite on every push. |
