from crucible_ast.static_inspector import analyze_python_submission


def test_clean_typed_linear_code_passes_all_checks() -> None:
    clean_code = '''
def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int]:
    left: int = 0
    right: int = len(nums) - 1
    while left < right:
        current: int = nums[left] + nums[right]
        if current == target:
            return (left, right)
        elif current < target:
            left += 1
        else:
            right -= 1
    return (-1, -1)
'''
    report = analyze_python_submission(clean_code)
    assert report.syntax_valid is True
    assert report.max_loop_nesting_depth == 1
    assert report.estimated_time_complexity == "O(N)"
    assert report.security_violations == []
    assert report.missing_type_annotations is False
    assert report.production_ready is True


def test_detects_sandbox_escape_infinite_loop_and_cubic_complexity() -> None:
    rogue_code = '''
import subprocess

def bad_solver(grid):
    while True:
        for i in grid:
            for j in i:
                eval("1 + 1")
'''
    report = analyze_python_submission(rogue_code)
    assert report.syntax_valid is True
    assert report.max_loop_nesting_depth == 3
    assert report.estimated_time_complexity == "O(N^3)"
    assert any("FORBIDDEN_IMPORT: subprocess" in v for v in report.security_violations)
    assert any("FORBIDDEN_BUILTIN_CALL: eval()" in v for v in report.security_violations)
    assert any("INFINITE_LOOP_RISK" in v for v in report.security_violations)
    assert report.production_ready is False
