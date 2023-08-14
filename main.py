import os
import re

def find_errors_in_html(content, file_path):
    """
    Поиск ошибок в HTML-содержимом.

    :param content: Содержимое HTML-файла (str).
    :param file_path: Путь к файлу (используется только для справки, str).
    :return: Список ошибок с номерами строк и самими ошибками [(int, str)].
    """
    errors = []

    # Ищем открывающие теги без атрибута i18n
    pattern_open = re.compile(r'<(p|button|h2|h)(?![^>]*\bi18n\b)[^>]*>')

    # Ищем закрывающие теги, содержащие символы кроме пробелов после имени тега
    pattern_close = re.compile(r'</\s*(p|button|h|h2)[a-zA-Z0-9]+\s*>')

    # Разбиваем содержимое файла на строки
    lines = content.splitlines()

    # Проходим по каждой строке, ищем ошибки и сохраняем их
    for line_number, line in enumerate(lines, 1):
        matches_open = pattern_open.finditer(line)
        matches_close = pattern_close.finditer(line)

        for match in matches_open:
            errors.append((line_number, match.group()))
        for match in matches_close:
            errors.append((line_number, match.group()))

    return errors

def main(directory_path):
    """
    Главная функция, проходит по всем HTML-файлам в указанной директории
    и выводит ошибки, связанные с отсутствием атрибута i18n или
    неправильными закрывающими тегами.

    :param directory_path: Путь к директории с HTML-файлами (str).
    """
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            # Обрабатываем только HTML-файлы
            if file_name.endswith('.html'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    errors = find_errors_in_html(content, file_path)
                    for line_number, error in errors:
                        print(f"Ошибка в файле: {file_path}")
                        print(f"Строка №{line_number}: {error}")
                        if '</' in error:
                            print("Проблема: Найден закрывающий тег с атрибутами или неправильной структурой.")
                            print("Решение: Убедитесь, что закрывающие теги не содержат атрибутов.")
                        else:
                            print("Проблема: Отсутствует атрибут i18n в открывающем теге.")
                            print("Решение: Добавьте атрибут i18n к открывающему тегу.")
                        print('-' * 80)  # Разделительная линия между ошибками

if __name__ == "__main__":
    main("..")
