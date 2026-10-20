import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateModelBenchmarkRun } from './leaderboard_ranker.mjs';

test('Layers 32-34: Crucible Leaderboard Ranker scores frontier models and disqualifies collapsed outputs', () => {
  const frontier = evaluateModelBenchmarkRun({
    modelId: 'frontier-coder-v4',
    passAt1: 0.84,
    astProductionReadyRatio: 0.96,
    mutationKillRatio: 0.91,
    duplicateHashRatio: 0.08
  });
  assert.equal(frontier.verdict, 'FRONTIER_TIER_APPROVED');
  assert.equal(frontier.compositeScore, 0.884);

  const collapsed = evaluateModelBenchmarkRun({
    modelId: 'overfit-model-v1',
    passAt1: 0.90,
    astProductionReadyRatio: 0.90,
    mutationKillRatio: 0.90,
    duplicateHashRatio: 0.95
  });
  assert.equal(collapsed.verdict, 'DISQUALIFIED_MEMORIZATION_OR_COLLAPSE');
  assert.equal(collapsed.compositeScore, 0.0);
});
