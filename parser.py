from urllib import response

import requests
from bs4 import BeautifulSoup
#Функция подготовки названия страны
def clear_str(text):
    if not text:
        return ''
    return text.strip().replace(' ', '_')
#Функция создания списка url
def list_url(file):
    urls = []
    with open(file, 'r') as f:
        for line in f:
            urls.append(f"https://en.wikipedia.org/wiki/{clear_str(line)}")
        return urls

# def parser():
#     urls = list_url('countries.txt')
#     if not urls:
#         print("Файл countries.txt пуст или не найден!")
#         return
#
#     # Берем пока только самую первую страну для теста
#     test_url = urls[0]
#     print(f"Запускаем тест для ссылки: {test_url}")
#
#     session = requests.Session()
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
#
#     response = session.get(test_url, headers=headers, timeout=10)
#     print(f"Код ответа от Википедии: {response.status_code}")
#
#     soup = BeautifulSoup(response.text, 'html.parser')
#     infobox = soup.find('table', class_='infobox')
#
#     if infobox:
#         print("\n--- Результаты парсинга infobox ---")
#         for row in infobox.find_all('tr'):
#             header = row.find('th')
#             value_td = row.find('td')
#
#             if header and value_td:
#                 header_text = header.text.strip().lower()
#
#                 # Ищем столицу (Capital)
#                 if 'capital' in header_text:
#                     print("Столица:", value_td.text.strip())
#
#                 # Ищем площадь (Area)
#                 if 'area' in header_text:
#                     print("Площадь (грязные данные):", value_td.text.strip())
#
#                 # Ищем население (Population)
#                 if 'population' in header_text:
#                     print("Население (основная строка):", value_td.text.strip())
#                     # Википедия часто переносит само число на строку ниже.
#                     # Давай проверим следующую строчку таблицы:
#                     next_row = row.find_next_sibling('tr')
#                     if next_row and next_row.find('td'):
#                         print("Население (значение ниже):", next_row.find('td').text.strip())
#     else:
#         print("Не удалось найти карточку 'infobox' на странице.")
#     session.close()
#
#
#
#
# if __name__ == "__main__":
#     parser()