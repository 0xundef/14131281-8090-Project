import sys
import os

# Add current directory to path so imports work
sys.path.append(os.path.dirname(__file__))

from skip_list import SkipList


def main():
    print("Starting Skip List demo...")
    sl = SkipList(max_level=8, p=0.5, seed=42)

    values = [7, 3, 9, 1, 5, 8, 2]
    print("Insert:", values)
    for x in values:
        sl.insert(x)

    print("\nSkip list levels (top -> bottom):")
    levels = sl.to_levels()
    for i in reversed(range(sl.level)):
        print(f"Level {i + 1}:", levels[i])

    print("\nSearch 5:", sl.search(5))
    print("Search 6:", sl.search(6))

    print("\nDelete 5:", sl.delete(5))
    print("Search 5:", sl.search(5))


if __name__ == "__main__":
    main()
