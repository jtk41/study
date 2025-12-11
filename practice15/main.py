class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if not node:
            return TreeNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node:
            return None
        if key == node.key:
            return node.value
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            temp = self._min_value_node(node.right)
            node.key, node.value = temp.key, temp.value
            node.right = self._delete(node.right, temp.key)
        if node:
            node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def height(self):
        return self._get_height(self.root)

    def _get_height(self, node):
        return node.height if node else 0

    def is_balanced(self):
        return self._is_balanced(self.root)

    def _is_balanced(self, node):
        if not node:
            return True
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)
        if abs(left_height - right_height) > 1:
            return False
        return self._is_balanced(node.left) and self._is_balanced(node.right)
    
bst = BinarySearchTree()

print("=== Вставка элементов ===")
bst.insert(50, "Apple")
bst.insert(30, "Banana")
bst.insert(70, "Cherry")
bst.insert(20, "Date")
bst.insert(40, "Elderberry")
bst.insert(60, "Fig")
bst.insert(80, "Grape")

print("Поиск существующего ключа 40:", bst.search(40))
print("Поиск несуществующего ключа 100:", bst.search(100))
print("Текущая высота дерева:", bst.height())
print("Дерево сбалансировано?", bst.is_balanced())

print("\n=== Вставка элемента с существующим ключом ===")
bst.insert(40, "Eggplant")
print("Ключ 40 после обновления:", bst.search(40))

print("\n=== Удаление узла с одним потомком ===")
bst.delete(20)
print("Поиск удаленного ключа 20:", bst.search(20))
print("Высота после удаления 20:", bst.height())

print("\n=== Удаление узла с двумя потомками ===")
bst.delete(50)
print("Поиск удаленного ключа 50:", bst.search(50))
print("Высота после удаления корня:", bst.height())

print("\n=== Проверка сбалансированности после операций ===")
print("Дерево сбалансировано?", bst.is_balanced())

print("\n=== Удаление всех элементов по одному ===")
keys_to_delete = [30, 40, 60, 70, 80]
for key in keys_to_delete:
    bst.delete(key)
    print(f"После удаления {key}: высота = {bst.height()}, сбалансировано = {bst.is_balanced()}")

print("\n=== Пустое дерево ===")
print("Высота пустого дерева:", bst.height())
print("Пустое дерево сбалансировано?", bst.is_balanced())

print("\n=== Добавление элементов в несбалансированное дерево ===")
bst2 = BinarySearchTree()
for i in range(1, 6):
    bst2.insert(i, f"Value{i}")
print("Высота вырожденного дерева:", bst2.height())
print("Дерево сбалансировано?", bst2.is_balanced())