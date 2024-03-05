#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os
from jsonschema import validate
from datetime import date

new_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "post": {"type": "string"},
        "year": {"type": "number"}
    },
    "required": ["name", "post", "year"],
}


def get_worker():
    """
    Запросить данные о работнике.
    """

    name = input("Фамилия и инициалы? ")
    post = input("Должность? ")
    year = int(input("Год поступления? "))

    worker_data = {'name': name, 'post': post, 'year': year}

    try:
        validate(instance=worker_data, schema=new_schema)
        return {
        'name': name,
        'post': post,
        'year': year,
        }
    except Exception as e:
        print("Ошибка данных")


def display_workers(staff):
    """
    Отобразить список работников.
    """

    if staff:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "№",
                "Ф.И.О.",
                "Должность",
                "Год"
            )
        )
        print(line)

        for idx, worker in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    worker.get('name', ''),
                    worker.get('post', ''),
                    worker.get('year', 0)
                )
            )
        print(line)

    else:
        print("Список работников пуст.")

def select_workers(staff, period):
    """
    Выбрать работников с заданным стажем.
    """

    today = date.today()

    result = []
    for employee in staff:
        if today.year - employee.get('year', today.year) >= period:
            result.append(employee)

    return result


def save_workers(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """

    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_workers(file_name):
    """
    Загрузить всех работников из файла JSON.
    """

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as fin:
            file_data = json.load(fin)
        try:
            for data in file_data:
                validate(instance=data, schema=new_schema)
            return file_data
        except Exception as e:
            print("Ошибка загрузки данных")
            return None
    else:
        print("Файл не существует")
        return None


def main():
    """
    Главная функция программы.
    """

    workers = []
    while True:
        command = input(">>> ").lower()

        if command == "exit":
            break

        elif command == "add":
            worker = get_worker()
            workers.append(worker)
            if len(workers) > 1:
                workers.sort(key=lambda item: item.get('name', ''))

        elif command == "list":
            display_workers(workers)

        elif command.startswith("select "):
            parts = command.split(maxsplit=1)
            period = int(parts[1])
            selected = select_workers(workers, period)
            display_workers(selected)

        elif command.startswith("save "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]

            save_workers(file_name, workers)

        elif command.startswith("load "):
            parts = command.split(maxsplit=1)
            file_name = parts[1]

            workers = load_workers(file_name)

        elif command == 'help':
            print("Список команд:\n")
            print("add - добавить работника;")
            print("list - вывести список работников;")
            print("select <стаж> - запросить работников со стажем;")
            print("help - отобразить справку;")
            print("load - загрузить данные из файла;")
            print("save - сохранить данные в файл;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)

if __name__ == '__main__':
    main()
