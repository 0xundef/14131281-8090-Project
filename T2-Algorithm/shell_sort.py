"""
Shell Sort implementation for self-study.

Shell sort is an in-place comparison sort that generalizes insertion sort by allowing
exchanges of elements that are far apart using a decreasing gap sequence.

This implementation uses Shell's original gap sequence: n//2, n//4, ..., 1.

Time complexity:
  - Depends on gap sequence.
  - Worst case can be O(n^2) for simple sequences.
  - Often performs much better than insertion sort in practice for medium sizes.
Space complexity: O(1) extra space (in-place).
"""

from __future__ import annotations

from typing import List, Tuple


def shell_sort(arr: List[int]) -> List[int]:
    """Return a new sorted list using shell sort (does not modify input)."""
    a = list(arr)
    n = len(a)
    gap = n // 2

    while gap > 0:
        # gapped insertion sort
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 2

    return a


def shell_sort_with_steps(arr: List[int]) -> Tuple[List[int], List[Tuple[int, List[int]]]]:
    """
    Sort and record intermediate arrays after each gap pass.
    Returns (sorted_list, steps) where steps is [(gap, snapshot), ...].
    """
    a = list(arr)
    n = len(a)
    steps: List[Tuple[int, List[int]]] = []

    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        steps.append((gap, list(a)))
        gap //= 2

    return a, steps

