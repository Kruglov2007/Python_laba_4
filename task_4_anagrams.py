def are_anagrams(a, b)->bool:
    """
       Проверяет, являются ли две строки анаграммами.

       Строки являются анаграммами, если состоят из одних и тех же букв
       с одинаковым количеством повторений, но в разном порядке.
       Регистр букв не учитывается.

       :param a: Первая строка.
       :param b: Вторая строка.
       :return: True, если строки — анаграммы, иначе False.
       """
    if not a or not b:
        return False
    a = a.lower()
    b = b.lower()
    if len(a) != len(b) or a==b:
        return False

    dict_a={}
    for letter in a:
        dict_a[letter]=dict_a.get(letter,0)+1
    dict_b = {}
    for letter in b:
        dict_b[letter] = dict_b.get(letter, 0) + 1
    anagram=True
    for key, value in dict_a.items():
        if dict_b.get(key, 0) != value:
            anagram=False
    for key, value in dict_b.items():
        if dict_a.get(key, 0) != value:
            anagram=False
    return anagram