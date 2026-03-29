class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)

        if self.root is None:
            self.root = new_node
            return

        current = self.root

        while True:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right

    def print_tree(self):
        if self.root is None:
            print("El árbol está vacío")
        else:
            self._print_in_order(self.root)

    def _print_in_order(self, node):
        if node is not None:
            self._print_in_order(node.left)
            print(node.value)
            self._print_in_order(node.right)


if __name__ == "__main__":
    tree = BinaryTree()

    tree.insert(50)
    tree.insert(30)
    tree.insert(70)
    tree.insert(20)
    tree.insert(40)
    tree.insert(60)
    tree.insert(80)

    print("Árbol binario:")
    tree.print_tree()