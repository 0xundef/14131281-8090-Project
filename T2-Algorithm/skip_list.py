"""
Skip List implementation for self-study.

Skip List is a probabilistic balanced search structure that supports:
  - search(x), insert(x), delete(x)
Average time complexity: O(log n)
Worst-case time complexity: O(n) (rare, depends on randomization)

This implementation stores *unique comparable keys* (like an ordered set).
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class _Node(Generic[T]):
    key: T
    forward: List[Optional["_Node[T]"]]  # forward pointers for each level


class SkipList(Generic[T]):
    def __init__(self, max_level: int = 16, p: float = 0.5, seed: int = 42) -> None:
        if max_level <= 0:
            raise ValueError("max_level must be positive")
        if not (0 < p < 1):
            raise ValueError("p must be between 0 and 1")

        self.max_level = max_level
        self.p = p
        self._rand = random.Random(seed)

        # Header uses a sentinel key; it won't be compared in traversal (we start from header)
        self.header: _Node[T] = _Node(key=None, forward=[None] * max_level)  # type: ignore[arg-type]
        self.level = 1  # current highest level (1..max_level)
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def _random_level(self) -> int:
        lvl = 1
        while lvl < self.max_level and self._rand.random() < self.p:
            lvl += 1
        return lvl

    def search(self, key: T) -> bool:
        cur = self.header
        # Traverse from top level down
        for i in reversed(range(self.level)):
            while cur.forward[i] is not None and cur.forward[i].key < key:
                cur = cur.forward[i]
        cur = cur.forward[0] if cur.forward[0] is not None else None
        return cur is not None and cur.key == key

    def insert(self, key: T) -> bool:
        """
        Insert a key into the skip list.
        Returns True if inserted, False if key already exists.
        """
        update: List[_Node[T]] = [self.header] * self.max_level
        cur = self.header

        for i in reversed(range(self.level)):
            while cur.forward[i] is not None and cur.forward[i].key < key:
                cur = cur.forward[i]
            update[i] = cur

        # check if exists at level 0
        nxt = cur.forward[0]
        if nxt is not None and nxt.key == key:
            return False

        node_level = self._random_level()
        if node_level > self.level:
            for i in range(self.level, node_level):
                update[i] = self.header
            self.level = node_level

        new_node = _Node(key=key, forward=[None] * node_level)
        for i in range(node_level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        self.size += 1
        return True

    def delete(self, key: T) -> bool:
        """
        Delete key if present.
        Returns True if deleted; False if not found.
        """
        update: List[_Node[T]] = [self.header] * self.max_level
        cur = self.header

        for i in reversed(range(self.level)):
            while cur.forward[i] is not None and cur.forward[i].key < key:
                cur = cur.forward[i]
            update[i] = cur

        target = cur.forward[0]
        if target is None or target.key != key:
            return False

        # Re-link pointers for each level present in target
        for i in range(self.level):
            if update[i].forward[i] is not target:
                continue
            update[i].forward[i] = target.forward[i] if i < len(target.forward) else None

        # Reduce level if top levels become empty
        while self.level > 1 and self.header.forward[self.level - 1] is None:
            self.level -= 1

        self.size -= 1
        return True

    def to_levels(self) -> List[List[T]]:
        """
        Return a list of levels for visualization:
        levels[0] is the bottom level; levels[level-1] is the current top.
        """
        levels: List[List[T]] = []
        for i in range(self.level):
            cur = self.header.forward[i]
            row: List[T] = []
            while cur is not None:
                row.append(cur.key)
                cur = cur.forward[i] if i < len(cur.forward) else None
            levels.append(row)
        return levels


def _demo() -> None:
    print("SkipList demo (ordered set)")
    sl = SkipList[int](max_level=8, p=0.5, seed=42)
    for x in [7, 3, 9, 1, 5, 8, 2]:
        sl.insert(x)

    print("\nLevels (top to bottom):")
    for lvl in reversed(range(sl.level)):
        print(f"Level {lvl + 1}:", sl.to_levels()[lvl])

    print("\nSearch examples:")
    for k in [5, 6]:
        print(f"search({k}) ->", sl.search(k))

    print("\nDelete 5:")
    sl.delete(5)
    print("search(5) ->", sl.search(5))


if __name__ == "__main__":
    _demo()

