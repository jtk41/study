# Пример использования

# Создание дерева
bst = BinarySearchTree()

# Вставка элементов
bst.insert(10, "Value10")
bst.insert(5, "Value5")
bst.insert(15, "Value15")
bst.insert(3, "Value3")
bst.insert(7, "Value7")

# Поиск элементов
print(bst.search(5))   # Вывод: Value5
print(bst.search(20))  # Вывод: None

# Высота дерева
print(bst.height())    # Вывод: 3

# Проверка сбалансированности
print(bst.is_balanced())  # Вывод: True

# Удаление элемента
bst.delete(5)
print(bst.search(5))   # Вывод: None

# Обновленная высота
print(bst.height())    # Вывод: 3 или меньше