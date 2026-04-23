class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            print("El stack está vacío")
            return None

        removed_value = self.top.value
        self.top = self.top.next
        return removed_value

    def print_stack(self):
        if self.top is None:
            print("El stack está vacío")
            return

        current = self.top
        while current is not None:
            print(current.value)
            current = current.next


if __name__ == "__main__":
    stack = Stack()

    stack.push(10)
    stack.push(20)
    stack.push(30)

    print("Stack:")
    stack.print_stack()

    print("Pop:", stack.pop())

    print("Después de pop:")
    stack.print_stack()