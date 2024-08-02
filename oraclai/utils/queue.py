from typing import Generic, TypeVar


from collections import deque
# if you want to use the queue in the multi-threading environment
# you should implement a blocking queue with a lock acquire/release over the queue


T = TypeVar('T')


class Queue(Generic[T]):
    """
    A Queue class implemented using deque.

    Attributes:
        items: A deque object to store the queue elements.
    """

    def __init__(self):
        """Initializes an empty queue."""
        self.items: deque[T] = deque()


    def reset(self):
        """Resets the queue by removing all elements."""
        self.items.clear()


    def is_empty(self) -> bool:
        """Checks if the queue is empty.

        Returns:
            True if the queue is empty, False otherwise.
        """
        return not self.items


    def enqueue(self, item: T):
        """Adds an item to the back of the queue.

        Args:
            item: The item to be added.
        """
        self.items.append(item)


    def dequeue(self) -> T:
        """Removes and returns the item from the front of the queue.

        Raises:
            IndexError: If the queue is empty.

        Returns:
            The item removed from the queue.
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self.items.popleft()


    def peek(self) -> T:
        """Returns the item at the front of the queue without removing it.

        Raises:
            IndexError: If the queue is empty.

        Returns:
            The item at the front of the queue.
        """
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self.items[0]


    def __len__(self) -> int:
        """Returns the number of items in the queue."""
        return len(self.items)
