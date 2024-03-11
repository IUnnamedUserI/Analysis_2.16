#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from datetime import datetime

def print_help():
    """
    Функция вывода доступных пользователю команд
    """
    
    print("list - вывод всех добавленных записей")
    print("add - добавление новых записей")
    print("find - найти запись по фамилии")
    print("exit - завершение работы программы")


def add():
    """
    Функция добавления новой записи, возвращает запись
    """
    
    surname = input("Введите фамилию: ")
    name = input("Введите имя: ")
    phone = input("Введите номер телефона: ")
    day, month, year = map(int, input("Введите дату рождения: ").split('.'))
    date = datetime(year, month, day).date().strftime('%d.%m.%Y')
    
    new_member = {'surname': surname,
                    'name': name,
                    'phone': phone,
                    'date': date
                }
    
    return new_member


def print_list(list):
    """
    Функция выводит на экран список всех существующих записей
    """
    
    for member in member_list:
        print(f"{member['surname']} {member['name']}, "
                f"{member['phone']}, {member['date']}")
        

def find_member(surname):
    """
    Функция для вывода на экран всех записей, чьи фамилии совпадают
    с введённой (не возвращает никаких значений)
    """
    
    count = 0

    for member in member_list:
        if member['surname'] == surname:
            print(f"{member['surname']} {member['name']}, "
                f"{member['phone']}, {member['date']}")
            count += 1
        
        if count == 0:
            print("Записи не найдены")


def save_file(filename, data):
    """
    Сохранение списка сотрудников в файл формата JSON
    """

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_file(filename):
    """
    Загрузка данных о сотрудниках из указанного JSON-файла
    """

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    """
    Основная программа
    """
    
    member_list = []

    while True:
        cmd = input(">>> ")

        if cmd == "help":
            print_help()

        elif cmd == "add":
            member_list.append(add())
            member_list.sort(key=lambda item: item.get('phone')[:3])

        elif cmd == "list":
            print_list(member_list)
                
        elif cmd == "find":
            find_member(input("Введите фамилию: "))

        elif cmd.startswith("save"):
            data = cmd.split(" ")
            save_file(data[1], member_list)

        elif cmd.startswith("load"):
            data = cmd.split(" ")
            member_list = load_file(data[1])

        elif cmd == "exit":
            print("Завершение работы программы...")
            break

        else:
            print(f"Команды {cmd} не существует")