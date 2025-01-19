import os
import requests
import sys

# Настройки
GITHUB_RAW_URL = "https://raw.githubusercontent.com/ignatieff/self-updating-script/main"
VERSION_FILE = "version.txt"
SCRIPT_FILE = "main.py"

def get_remote_version():
    """Получить версию из GitHub."""
    url = f"{GITHUB_RAW_URL}/{VERSION_FILE}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception(f"Ошибка получения версии: {response.status_code}")

def get_local_version():
    """Получить локальную версию."""
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as file:
            return file.read().strip()
    return None

def update_script():
    """Скачать и обновить скрипт."""
    url = f"{GITHUB_RAW_URL}/{SCRIPT_FILE}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(SCRIPT_FILE, "wb") as file:
            file.write(response.content)
        print("Скрипт обновлен.")
    else:
        raise Exception(f"Ошибка загрузки скрипта: {response.status_code}")

def update_version_file(remote_version):
    """Обновить локальный файл версии."""
    with open(VERSION_FILE, "w") as file:
        file.write(remote_version)

def main():
    try:
        local_version = get_local_version()
        remote_version = get_remote_version()

        if local_version != remote_version:
            print(f"Новая версия обнаружена: {remote_version}. Обновление...")
            update_script()
            update_version_file(remote_version)
            print("Перезапуск скрипта...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("Вы используете последнюю версию.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()