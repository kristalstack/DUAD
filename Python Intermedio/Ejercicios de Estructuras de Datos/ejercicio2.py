class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def push_left(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def push_right(self, value):
        new_node = Node(value)

        if self.tail is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def pop_left(self):
        if self.head is None:
            print("El deque está vacío")
            return None

        value = self.head.value
        self.head = self.head.next

        if self.head is not None:
            self.head.prev = None
        else:
            self.tail = None

        return value

    def pop_right(self):
        if self.tail is None:
            print("El deque está vacío")
            return None

        value = self.tail.value
        self.tail = self.tail.prev

        if self.tail is not None:
            self.tail.next = None
        else:
            self.head = None

        return value

    def print_deque(self):
        if self.head is None:
            print("El deque está vacío")
            return

        current = self.head
        while current is not None:
            print(current.value)
            current = current.next


if __name__ == "__main__":
    dq = Deque()

    dq.push_left(10)
    dq.push_left(20)
    dq.push_right(30)
    dq.push_right(40)

    print("Deque:")
    dq.print_deque()

    print("pop_left:", dq.pop_left())
    print("pop_right:", dq.pop_right())

    print("Después de pops:")
    dq.print_deque()