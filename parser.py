import requests
from bs4 import BeautifulSoup
import csv
import argparse
import os
import time
import re

#Функция подготовки названия страны
def clear_str(text):
    if not text:
        return ''
    return text.strip().replace(' ', '_')

## Функция очистки числовых значений
def clean_number(text):
    text = text.replace(',', '').replace(' ', '')
    match = re.search(r'\d+', text)

    if match:
        return match.group()

    return ''

#Функция создания списка url
def list_url(file):
    urls = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                clean_line = clear_str(line)
                if clean_line:
                    urls.append(f"https://en.wikipedia.org/wiki/{clean_line}")
        return urls
    except FileNotFoundError:
        return urls


def parser(input_file='countries.txt', output_file='countries_data.csv'):
    urls = list_url(input_file)
    if not urls:
        print(f"Файл {input_file} пуст или не найден!")
        return
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    session = requests.Session()
    data=[]
    os.makedirs('cache', exist_ok=True)
    for url in urls:
        city = ''
        area = ''
        population = ''
        country = url.split('/')[-1].replace('_', ' ')
        cache_file = os.path.join('cache', country.replace(' ', '_') + '.html')
        print(f"\nЗапускаем тест для ссылки: {url}")
        try:
            if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
                print(f"Загружаем страницу из кэша: {cache_file}")
                with open(cache_file, "r", encoding="utf-8") as file:
                    html=file.read()
            else:
                print("Страницы нет в кэше. Загружаем из Википедии.")
                response = session.get(url, headers=headers, timeout=10)
                time.sleep(1)
                print(f"Код ответа от Википедии: {response.status_code}")

                if response.status_code != 200:
                    print(f"Не удалось загрузить страницу: {url}")
                    data.append([country, city, area, population])
                    continue

                html = response.text
                with open(cache_file, "w", encoding="utf-8") as file:
                    file.write(html)
                print(f"Страница сохранена в кэш: {cache_file}")
            soup=BeautifulSoup(html, "html.parser")
            infobox = soup.find("table", class_="infobox")

            if infobox:
                print("--- Результаты парсинга infobox ---")

                # Флаги для отслеживания
                parsing_area_section = False
                parsing_pop_section = False
                area_found = False
                pop_found = False

                for row in infobox.find_all("tr"):
                    header = row.find("th")
                    value_td = row.find("td")

                    if not header:
                        continue

                    header_text = header.text.strip().lower()

                    # СЦЕНАРИЙ 1: Заголовок-подраздел БЕЗ значения в текущей строке (Канада)
                    if not value_td:
                        if "area" in header_text:
                            parsing_area_section = True
                            parsing_pop_section = False
                        elif "population" in header_text:
                            parsing_pop_section = True
                            parsing_area_section = False
                        elif header.get('colspan') or 'infobox-header' in header.get('class', []):
                            parsing_area_section = False
                            parsing_pop_section = False
                        continue

                    # СЦЕНАРИЙ 2: Строка содержит и заголовок, и значение <td>
                    clean_value = value_td.text

                    # --- ПОИСК СТОЛИЦЫ ---
                    if "capital" in header_text and not (parsing_area_section or parsing_pop_section):
                        a_tag = value_td.find('a')
                        city = a_tag.text.strip() if a_tag else value_td.text.strip()
                        print(f"Столица: {city}")

                    # --- ПОИСК ПЛОЩАДИ (С ОГРАНИЧИТЕЛЕМ) ---
                    elif (parsing_area_section or "area" in header_text) and not area_found:

                        if "land" not in header_text and "metropolitan" not in header_text:
                            if "total" in header_text or header_text == "area":
                                area = clean_number(clean_value)
                                print(f"Площадь: {area}")
                                area_found = True  # Блокируем дальнейший поиск площади для этой страны
                                parsing_area_section = False

                    # --- ПОИСК НАСЕЛЕНИЯ (С ОГРАНИЧИТЕЛЕМ) ---
                    elif (parsing_pop_section or "estimate" in header_text) and not pop_found:
                        if "estimate" in header_text:
                            # Строго игнорируем строки с уточнением "metropolitan" (как у Франции)
                            if "metropolitan" not in header_text:
                                for word in ["increase", "decrease", "neutral"]:
                                    clean_value = clean_value.lower().replace(word, "").strip()

                                population =clean_number(clean_value)
                                print(f"Население : {population}")
                                pop_found = True  # Блокируем дальнейший поиск населения для этой страны
                                parsing_pop_section = False
                data.append([country,city, area, population])
            else:
                print("Не удалось найти карточку 'infobox' на странице.")
                data.append([country, city, area, population])
                continue

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к {url}: {e}")
            data.append([country, city, area, population])
    with open(output_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["country","city","area","population"])
        writer.writerows(data)

    session.close()


if __name__ == "__main__":
    argument_parser=argparse.ArgumentParser()
    argument_parser.add_argument(
        '--input',
        default='countries.txt',
        help='Имя входного файла'
    )
    argument_parser.add_argument(
        '--output',
        default='countries_data.csv',
        help='Имя выходного файла'
    )
    args = argument_parser.parse_args()
    parser(args.input, args.output)
