"""
Скрипт для автоматической установки зависимостей путем запуска подпроцессов
и установки шрифта для приложения с помощью менеджера шрифтов matplotlib
"""

import subprocess
import os
import matplotlib.font_manager as fm

# Установка зависимостей
try:
    with open('requirements.txt', 'r') as file:
        dependencies = file.read().splitlines()

    # Install each dependency using pip
    for dependency in dependencies:
        subprocess.check_call(['pip', 'install', dependency])

    print("Все зависимости установлены!")
except FileNotFoundError:
    print("requirements.txt не найден.")
except subprocess.CalledProcessError as e:
    print(f"Ошибка при установке зависимостей: {e}")

# Установка шрифта
try:
    # Получение пути к директории шрифтов системы
    font_file = "HYWenHei.ttf"
    font_dir = fm.get_home()

    # Копирование файла шрифта в директорию шрифтов
    font_path = os.path.join(font_dir, font_file)
    with open(font_file, 'rb') as source_file:
        with open(font_path, 'wb') as dest_file:
            dest_file.write(source_file.read())

    # Перестройка кэша шрифтов
    fm._rebuild()

    print(f"Шрифт установлен успешно!")
except FileNotFoundError:
    print(f"Файл шрифта не найден.")
except PermissionError:
    print(f"Доступ запрещен. Установка шрифта не была завершена.")
except Exception as e:
    print(f"Ошибка при установке шрифта: {e}")

