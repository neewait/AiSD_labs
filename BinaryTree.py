class BinaryTree:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def has_child(self):
        return self.left is not None or self.right is not None


class BinarySearchTree:
    def __init__(self):
        self.start = None

    def search(self, key):
        node = self.find_node(key)
        return node.value if node else None

    def find_node(self, key):
        node = self.start
        while node:
            if node.key == key:
                return node
            node = node.right if key > node.key else node.left
        return None

    def set(self, k, v):
        node = self.find_node(k)
        if node:
            node.value = v
        else:
            return "error"
        return None

    def add(self, new_node):
        if self.find_node(new_node.key):
            return "error"
        if self.start is None:
            self.start = new_node
            return None

        node = self.start
        while True:
            if new_node.key > node.key:
                if node.right:
                    node = node.right
                else:
                    node.right = new_node
                    new_node.parent = node
                    return None
            else:
                if node.left:
                    node = node.left
                else:
                    node.left = new_node
                    new_node.parent = node
                    return None

    def _max(self, node):
        current = node
        while current and current.right:
            current = current.right
        return current

    def max(self):
        if self.start:
            max_node = self._max(self.start)
            return (max_node.key, max_node.value)
        return "error"

    def _min(self, node):
        current = node
        while current and current.left:
            current = current.left
        return current

    def min(self):
        if self.start:
            min_node = self._min(self.start)
            return (min_node.key, min_node.value)
        return "error"

    def delete(self, key):
        node = self.find_node(key)
        if node:
            self.delete_node(node)
            return None
        return "error"

    def delete_node(self, node):
        if not node.has_child():
            if node != self.start:
                if node.parent.left == node:
                    node.parent.left = None
                else:
                    node.parent.right = None
            else:
                self.start = None
        elif node.left and node.right:
            max_node = self._max(node.left)
            node.key = max_node.key
            node.value = max_node.value
            self.delete_node(max_node)
        else:
            child = node.left if node.left else node.right
            if node != self.start:
                if node == node.parent.left:
                    node.parent.left = child
                else:
                    node.parent.right = child
            else:
                self.start = child
            if child:
                child.parent = node.parent

    def print_tree(self):
        if not self.start:
            return "_"

        queue = [self.start]
        is_first_level = True
        output = []

        while queue:
            level_size = len(queue)
            level_output = []

            for _ in range(level_size):
                current = queue.pop(0)
                if current:
                    if is_first_level:
                        level_output.append(f"[{current.key} {current.value}]")
                    else:
                        parent_key = str(current.parent.key) if current.parent else "_"

                        level_output.append(f"[{current.key} {current.value} {parent_key}]")
                    queue.append(current.left)
                    queue.append(current.right)
                else:
                    level_output.append("_")
                    queue.extend([None, None])

            output.append(" ".join(level_output).strip())
            is_first_level = False

            if all(node is None for node in queue):
                break

        return "\n".join(output)


def main():
    tree = BinarySearchTree()
    while True:
        try:
            input_line = input().strip()
            if not input_line:
                continue
            parts = input_line.split()
            if len(parts) == 3:
                command, key, value = parts[0], int(parts[1]), parts[2]
                if command == "add":
                    result = tree.add(BinaryTree(key, value))
                    if result:
                        print(result)
                elif command == "set":
                    result = tree.set(key, value)
                    if result:
                        print(result)
                else:
                    print("error")
            elif len(parts) == 2:
                command, key = parts[0], int(parts[1])
                if command == "delete":
                    result = tree.delete(key)
                    if result:
                        print(result)
                elif command == "search":
                    result = tree.search(key)
                    if result:
                        print(f"1 {result}")
                    else:
                        print("0")
                else:
                    print("error")
            elif len(parts) == 1:
                command = parts[0]
                if command == "min":
                    result = tree.min()
                    if result != "error":
                        print(f"{result[0]} {result[1]}")
                    else:
                        print(result)
                elif command == "max":
                    result = tree.max()
                    if result != "error":
                        print(f"{result[0]} {result[1]}")
                    else:
                        print(result)
                elif command == "print":
                    result = tree.print_tree()
                    print(result)
                else:
                    print("error")
            else:
                print("error")
        except Exception:
            break


if __name__ == "__main__":
    main()
