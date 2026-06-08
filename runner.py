import sys
import io
import json
import traceback
import builtins
from typing import Any, Dict, List

def run_solution(user_code: str, problem_title: str,
                 test_cases: List[Dict]) -> List[Dict]:
    """
    Execute user code against test cases safely.
    Returns list of results per test case.
    """
    results = []

    # Detect entry function from problem title
    func_name = _get_func_name(problem_title)

    for tc in test_cases:
        inp      = tc.get('input', {})
        expected = tc.get('expected')
        result   = {
            'input':    inp,
            'expected': expected,
            'output':   None,
            'passed':   False,
            'error':    None
        }

        try:
            namespace = {}
            exec(compile(user_code, '<user>', 'exec'), namespace)

            if func_name not in namespace:
                # Try to find any callable
                funcs = [k for k, v in namespace.items()
                         if callable(v) and not k.startswith('_')]
                if not funcs:
                    result['error'] = f'No function found. Expected: {func_name}'
                    results.append(result)
                    continue
                func_name = funcs[0]

            fn     = namespace[func_name]
            output = fn(**inp)

            result['output'] = output
            result['passed'] = _compare(output, expected)

        except Exception as e:
            result['error'] = traceback.format_exc(limit=3)

        results.append(result)

    return results


def _get_func_name(title: str) -> str:
    """Map problem title to expected function name."""
    mapping = {
        'Two Sum':                  'twoSum',
        'Reverse a String':         'reverseString',
        'Valid Parentheses':        'isValid',
        'Maximum Subarray':         'maxSubArray',
        'Climbing Stairs':          'climbStairs',
        'Binary Search':            'search',
        'Merge Two Sorted Lists':   'mergeTwoLists',
        'Number of Islands':        'numIslands',
        'Fibonacci Number':         'fib',
        'Longest Common Prefix':    'longestCommonPrefix',
    }
    return mapping.get(title, 'solution')


def _compare(output: Any, expected: Any) -> bool:
    """Flexible comparison handling lists, sets, etc."""
    if isinstance(expected, list) and isinstance(output, list):
        # For Two Sum — order might differ
        return sorted(output) == sorted(expected)
    return output == expected