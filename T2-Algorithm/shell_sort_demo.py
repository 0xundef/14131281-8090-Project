import sys
import os

# Add current directory to path so imports work
sys.path.append(os.path.dirname(__file__))

from shell_sort import shell_sort_with_steps


def main():
    print("Starting Shell Sort demo...")
    arr = [23, 12, 1, 8, 34, 54, 2, 3]
    print("Original:", arr)

    sorted_arr, steps = shell_sort_with_steps(arr)

    print("\nSteps (after each gap pass):")
    for gap, snapshot in steps:
        print(f"gap={gap}: {snapshot}")

    print("\nSorted:", sorted_arr)


if __name__ == "__main__":
    main()

