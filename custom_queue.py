from collections import deque


class Queue:
    def __init__(self):
        self._items = deque([])

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        self._items.popleft()
    def is_empty(self):
        return not bool(self._items)

    def peek(self):
        return self._items[0]

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def __iter__(self):
        yield from self._items
