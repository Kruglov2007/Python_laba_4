def is_palindrome(value)->bool:
    """
       Принимает слово или число и возвращает True, если значение одинаково
       читается слева направо и справа налево. Регистр букв не учитывается.

       :param value: Строка или целое число для проверки.
       :return: True, если палиндром, иначе False.
       """
    if not value:
        return True
    value = str(value).lower()
    return value == value[::-1]