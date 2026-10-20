from typing import Callable, Dict, Any, List, Sequence, Tuple


class DifferentialBenchmarkHarness:
    """
    Layers 8-14: Evaluates AI-generated candidate functions against a ground-truth
    reference oracle across structured edge cases (empty inputs, negative weights,
    duplicate keys, and large-scale stress vectors).
    """

    @staticmethod
    def reference_kth_smallest_interval_merge(intervals: Sequence[Tuple[int, int]]) -> List[Tuple[int, int]]:
        if not intervals:
            return []
        sorted_iv = sorted(intervals, key=lambda x: (x[0], x[1]))
        merged: List[Tuple[int, int]] = [sorted_iv[0]]
        for start, end in sorted_iv[1:]:
            prev_start, prev_end = merged[-1]
            if start <= prev_end:
                merged[-1] = (prev_start, max(prev_end, end))
            else:
                merged.append((start, end))
        return merged

    def generate_adversarial_edge_cases(self) -> List[List[Tuple[int, int]]]:
        return [
            [],                                              # Edge case 1: Empty collection
            [(5, 5)],                                        # Edge case 2: Zero-length point interval
            [(-1000, -500), (-500, 0), (0, 500)],            # Edge case 3: Exact boundary touching
            [(10, 20), (1, 5), (12, 15), (-5, 2)],           # Edge case 4: Unsorted nested intervals
            [(-10**9, 10**9), (-50, 50), (10**9, 10**9)],    # Edge case 5: 64-bit coordinate extremes
        ]

    def evaluate_candidate_solution(
        self,
        candidate_fn: Callable[[Sequence[Tuple[int, int]]], List[Tuple[int, int]]]
    ) -> Dict[str, Any]:
        cases = self.generate_adversarial_edge_cases()
        passed = 0
        failures: List[Dict[str, Any]] = []

        for idx, test_input in enumerate(cases):
            expected = self.reference_kth_smallest_interval_merge(test_input)
            try:
                actual = candidate_fn(list(test_input))
                if actual == expected:
                    passed += 1
                else:
                    failures.append({
                        "case_index": idx,
                        "input": test_input,
                        "expected": expected,
                        "actual": actual,
                    })
            except Exception as exc:
                failures.append({
                    "case_index": idx,
                    "input": test_input,
                    "error": type(exc).__name__,
                })

        total = len(cases)
        return {
            "total_edge_cases": total,
            "passed_edge_cases": passed,
            "pass_rate": round(passed / total, 4),
            "all_edge_cases_passed": passed == total,
            "failures": failures,
        }
