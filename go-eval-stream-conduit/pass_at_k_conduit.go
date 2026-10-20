package main

import (
"crypto/sha256"
"encoding/hex"
"math"
"strings"
)

// Layers 15-17: Exact Unbiased Pass@k Estimator (Chen et al. Codex formulation)
// Computes 1 - C(n-c, k) / C(n, k) without factorial overflow.
func EstimateUnbiasedPassAtK(n int, c int, k int) float64 {
if n <= 0 || k <= 0 || k > n {
return 0.0
}
if n-c < k {
return 1.0
}
product := 1.0
for i := n - c + 1; i <= n; i++ {
product *= 1.0 - float64(k)/float64(i)
}
return math.Round((1.0-product)*10000) / 10000
}

// Layers 18-20: Scalable Evaluation Data Pipeline Deduplicator & Contamination Filter
type ModelCompletionRecord struct {
TaskID        string
ModelID       string
RawCompletion string
PassedTests   bool
}

type PipelineBatchSummary struct {
TotalIngested      int
UniqueCompletions  int
DuplicateCount     int
UnbiasedPassAt1    float64
UnbiasedPassAt5    float64
}

func ProcessEvaluationStreamBatch(records []ModelCompletionRecord) PipelineBatchSummary {
seenHashes := make(map[string]bool)
uniqueCount := 0
correctCount := 0

for _, rec := range records {
normalized := strings.Join(strings.Fields(rec.RawCompletion), " ")
digest := sha256.Sum256([]byte(rec.TaskID + "|" + normalized))
hashHex := hex.EncodeToString(digest[:])

if !seenHashes[hashHex] {
seenHashes[hashHex] = true
uniqueCount++
}
if rec.PassedTests {
correctCount++
}
}

total := len(records)
return PipelineBatchSummary{
TotalIngested:     total,
UniqueCompletions: uniqueCount,
DuplicateCount:    total - uniqueCount,
UnbiasedPassAt1:   EstimateUnbiasedPassAtK(total, correctCount, 1),
UnbiasedPassAt5:   EstimateUnbiasedPassAtK(total, correctCount, 5),
}
}
