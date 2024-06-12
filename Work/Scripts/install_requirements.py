"""
Скрипт для автоматической установки зависимостей путем запуска подпроцессов
"""

import subprocess


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

