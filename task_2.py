import csv
from BTrees.OOBTree import OOBTree
from timeit import timeit


# Завантаження даних із CSV файлу
def load_data(filename):
    items = []
    with open(filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["ID"] = int(row["ID"])
            row["Price"] = float(row["Price"])
            items.append(row)
    return items


# Ключем у дереві буде композитний ключ: (Price, ID)
def add_item_to_tree(tree, item):
    key = (item["Price"], item["ID"])
    tree[key] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }


def add_item_to_dict(dictionary, item):
    # Для dict залишаємо ключ ID
    dictionary[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"],
    }


# Діапазонний запит для дерева: використовуємо метод items,
def range_query_tree(tree, min_price, max_price):
    # Формуємо ключові межі:
    # Для нижньої межі – (min_price, мінімальне можливе значення для ID)
    # Для верхньої межі – (max_price, максимально можливе значення для ID)
    min_key = (min_price, 0)
    max_key = (max_price, float("inf"))
    return list(tree.items(min_key, max_key))


# Для словника реалізуємо діапазонний запит лінійним пошуком
def range_query_dict(dictionary, min_price, max_price):
    return [
        (key, value)
        for key, value in dictionary.items()
        if min_price <= value["Price"] <= max_price
    ]


if __name__ == "__main__":
    filename = "generated_items_data.csv"
    items = load_data(filename)

    tree = OOBTree()
    dictionary = {}

    # Додавання товарів до обох структур
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Параметри діапазонного запиту за ціною
    min_price = 10.0
    max_price = 50.0

    # Вимірюємо час виконання 100 запитів для кожної структури
    tree_time = timeit(lambda: range_query_tree(tree, min_price, max_price), number=100)
    dict_time = timeit(
        lambda: range_query_dict(dictionary, min_price, max_price), number=100
    )

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
