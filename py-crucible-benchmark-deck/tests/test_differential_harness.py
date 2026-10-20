from crucible_bench.differential_harness import DifferentialBenchmarkHarness


def test_reference_oracle_and_buggy_ai_candidate_detection() -> None:
    harness = DifferentialBenchmarkHarness()

    perfect_result = harness.evaluate_candidate_solution(
        harness.reference_kth_smallest_interval_merge
    )
    assert perfect_result["all_edge_cases_passed"] is True
    assert perfect_result["pass_rate"] == 1.0

    def flawed_ai_merge(intervals):
        if not intervals:
            return []
        s = sorted(intervals)
        out = [s[0]]
        for a, b in s[1:]:
            if a < out[-1][1]:
                out[-1] = (out[-1][0], max(out[-1][1], b))
            else:
                out.append((a, b))
        return out

    flawed_result = harness.evaluate_candidate_solution(flawed_ai_merge)
    assert flawed_result["all_edge_cases_passed"] is False
    assert len(flawed_result["failures"]) >= 1
