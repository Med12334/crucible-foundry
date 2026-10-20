package main

import "testing"

func TestEstimateUnbiasedPassAtKExactCombinatorics(t *testing.T) {
// If n=10 samples and c=5 passed:
// pass@1 = 5/10 = 0.5
p1 := EstimateUnbiasedPassAtK(10, 5, 1)
if p1 != 0.5 {
t.Fatalf("Expected Pass@1 to be 0.5, got %v", p1)
}

// pass@5 with n=10, c=5 should be 1 - C(5,5)/C(10,5) = 1 - 1/252 = 0.9960
p5 := EstimateUnbiasedPassAtK(10, 5, 5)
if p5 < 0.995 || p5 > 0.997 {
t.Fatalf("Expected Pass@5 to be ~0.9960, got %v", p5)
}
}

func TestProcessEvaluationStreamBatchDeduplicatesAndScores(t *testing.T) {
batch := []ModelCompletionRecord{
{TaskID: "CRUCIBLE-01", ModelID: "frontier-x", RawCompletion: "def solve(x):\n  return x + 1", PassedTests: true},
{TaskID: "CRUCIBLE-01", ModelID: "frontier-x", RawCompletion: "def solve(x):   return x + 1", PassedTests: true},
{TaskID: "CRUCIBLE-01", ModelID: "frontier-x", RawCompletion: "def solve(x): return x - 1", PassedTests: false},
{TaskID: "CRUCIBLE-01", ModelID: "frontier-x", RawCompletion: "def solve(x): return x * 2", PassedTests: false},
{TaskID: "CRUCIBLE-01", ModelID: "frontier-x", RawCompletion: "def solve(x): return 0", PassedTests: false},
}

summary := ProcessEvaluationStreamBatch(batch)
if summary.TotalIngested != 5 || summary.UniqueCompletions != 4 || summary.DuplicateCount != 1 {
t.Fatalf("Unexpected deduplication counts: %+v", summary)
}
if summary.UnbiasedPassAt1 != 0.4 {
t.Fatalf("Expected Pass@1 = 0.4, got %v", summary.UnbiasedPassAt1)
}
}
