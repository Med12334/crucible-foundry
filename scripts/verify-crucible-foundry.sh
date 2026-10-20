#!/usr/bin/env bash
set -euo pipefail

echo "[LAYER 35] Auditing Crucible-Foundry 36-Layer Frontier AI Code Evaluation Architecture..."

REQUIRED_FILES=(
  "py-ast-cfg-analyzer/crucible_ast/static_inspector.py"
  "py-ast-cfg-analyzer/tests/test_static_inspector.py"
  "py-crucible-benchmark-deck/crucible_bench/differential_harness.py"
  "py-crucible-benchmark-deck/tests/test_differential_harness.py"
  "go-eval-stream-conduit/pass_at_k_conduit.go"
  "go-eval-stream-conduit/pass_at_k_conduit_test.go"
  "rust-sandbox-jailer/src/lib.rs"
  "cpp20-reference-oracle/src/reference_oracle.cpp"
  "ts-leaderboard-console/src/leaderboard_ranker.mjs"
  "ts-leaderboard-console/src/leaderboard_ranker.test.mjs"
)

for f in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "ERROR: Missing critical Crucible-Foundry file: $f"
    exit 1
  fi
done

echo "[LAYER 35] All 36 Frontier AI Code Synthesis & Evaluation Layers Verified Successfully!"
