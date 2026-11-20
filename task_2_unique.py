def find_unique(items: list) -> list:
    """
    Принимает список и возвращает список элементов, встречающихся
    в исходном списке ровно один раз, в порядке их первого появления.

    :param items: Исходный список элементов.
    :return: Новый список, содержащий элементы, встретившиеся ровно 1 раз.
    """
    if not items or not isinstance(items, list):
        return []

    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1

    return [item for item in items if counts[item] == 1]
